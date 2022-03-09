import dataclasses
import re
from typing import Optional, Sequence, Type, TypeVar

from ._compat import get_args, get_origin, is_generic, is_sequence


@dataclasses.dataclass(frozen=True)
class AttributeOverride:
    omit_if_default: Optional[bool] = dataclasses.field(default=None)


def override(omit_if_default=None):
    return AttributeOverride(omit_if_default=omit_if_default)


_neutral = AttributeOverride()


def make_dict_unstructure_fn(cl, converter, omit_if_default=False, **kwargs):
    """Generate a specialized dict unstructuring function for a class."""
    cl_name = cl.__name__
    fn_name = "unstructure_" + cl_name
    globs = {"__c_u": converter.unstructure}
    lines = []
    post_lines = []

    fields = cl.__dataclass_fields__  # type: ignore

    lines.append("def {}(i):".format(fn_name))
    lines.append("    res = {")
    for field_name, f in fields.items():
        override = kwargs.pop(field_name, _neutral)
        default = f.default
        default_factory = f.default_factory
        if f.type is None:
            # No type annotation, doing runtime dispatch.
            if (
                (default is not dataclasses.MISSING)
                or (default_factory is not dataclasses.MISSING)
            ) and (
                (omit_if_default and override.omit_if_default is not False)
                or override.omit_if_default
            ):
                def_name = "__cattr_def_{}".format(field_name)

                if default_factory != dataclasses.MISSING:
                    globs[def_name] = default_factory
                    post_lines.append(
                        "    if i.{name} != {def_name}():".format(
                            name=field_name, def_name=def_name
                        )
                    )
                    post_lines.append(
                        "        res['{name}'] = i.{name}".format(
                            name=field_name
                        )
                    )
                else:
                    globs[def_name] = default
                    post_lines.append(
                        "    if i.{name} != {def_name}:".format(
                            name=field_name, def_name=def_name
                        )
                    )
                    post_lines.append(
                        "        res['{name}'] = __c_u(i.{name})".format(
                            name=field_name
                        )
                    )

            else:
                # No default or no override.
                lines.append(
                    "        '{name}': __c_u(i.{name}),".format(
                        name=field_name
                    )
                )
        else:
            # Do the dispatch here and now.
            type = f.type
            if is_sequence(type):
                type = Sequence
            conv_function = converter._unstructure_func.dispatch(type)
            if (
                (default is not dataclasses.MISSING)
                or (default_factory is not dataclasses.MISSING)
            ) and (
                (omit_if_default and override.omit_if_default is not False)
                or override.omit_if_default
            ):
                def_name = "__cattr_def_{}".format(field_name)

                if default_factory != dataclasses.MISSING:
                    # The default is computed every time.
                    globs[def_name] = default_factory
                    post_lines.append(
                        "    if i.{name} != {def_name}():".format(
                            name=field_name, def_name=def_name
                        )
                    )
                    if conv_function == converter._unstructure_identity:
                        # Special case this, avoid a function call.
                        post_lines.append(
                            "        res['{name}'] = i.{name}".format(
                                name=field_name
                            )
                        )
                    else:
                        unstruct_fn_name = "__cattr_unstruct_{}".format(
                            field_name
                        )
                        globs[unstruct_fn_name] = conv_function
                        post_lines.append(
                            "        res['{name}'] = {fn}(i.{name}),".format(
                                name=field_name, fn=unstruct_fn_name
                            )
                        )
                else:
                    # Default is not a factory, but a constant.
                    globs[def_name] = default
                    post_lines.append(
                        "    if i.{name} != {def_name}:".format(
                            name=field_name, def_name=def_name
                        )
                    )
                    if conv_function == converter._unstructure_identity:
                        post_lines.append(
                            "        res['{name}'] = i.{name}".format(
                                name=field_name
                            )
                        )
                    else:
                        unstruct_fn_name = "__cattr_unstruct_{}".format(
                            field_name
                        )
                        globs[unstruct_fn_name] = conv_function
                        post_lines.append(
                            "        res['{name}'] = {fn}(i.{name})".format(
                                name=field_name, fn=unstruct_fn_name
                            )
                        )
            else:
                # No omitting of defaults.
                if conv_function == converter._unstructure_identity:
                    # Special case this, avoid a function call.
                    lines.append(
                        "    '{name}': i.{name},".format(name=field_name)
                    )
                else:
                    unstruct_fn_name = "__cattr_unstruct_{}".format(field_name)
                    globs[unstruct_fn_name] = conv_function
                    lines.append(
                        "    '{name}': {fn}(i.{name}),".format(
                            name=field_name, fn=unstruct_fn_name
                        )
                    )
    lines.append("    }")

    total_lines = lines + post_lines + ["    return res"]

    eval(compile("\n".join(total_lines), "", "exec"), globs)

    fn = globs[fn_name]

    return fn


def generate_mapping(cl: Type, old_mapping):
    mapping = {}
    for p, t in zip(get_origin(cl).__parameters__, get_args(cl)):
        if isinstance(t, TypeVar):
            continue
        mapping[p.__name__] = t

    if not mapping:
        return old_mapping

    cls = dataclasses.make_dataclass(
        "GenericMapping",
        mapping.keys(),
        frozen=True,
    )

    return cls(**mapping)


def make_dict_structure_fn(cl: Type, converter, **kwargs):
    """Generate a specialized dict structuring function for an attrs class."""

    mapping = None
    if is_generic(cl):
        base = get_origin(cl)
        mapping = generate_mapping(cl, mapping)
        cl = base

    for base in getattr(cl, "__orig_bases__", ()):
        if is_generic(base) and not str(base).startswith("typing.Generic"):
            mapping = generate_mapping(base, mapping)
            break

    if isinstance(cl, TypeVar):
        cl = getattr(mapping, cl.__name__, cl)

    cl_name = cl.__name__
    fn_name = "structure_" + cl_name

    # We have generic parameters and need to generate a unique name for the function
    for p in getattr(cl, "__parameters__", ()):
        # This is nasty, I am not sure how best to handle
        # `typing.List[str]` or `TClass[int, int]` as a parameter type here
        name_base = getattr(mapping, p.__name__)
        name = getattr(name_base, "__name__", str(name_base))
        name = re.sub(r"[\[\.\] ,]", "_", name)
        fn_name += f"_{name}"

    globs = {"__c_s": converter.structure, "__cl": cl, "__m": mapping}
    lines = []
    post_lines = []

    attrs = dataclasses.fields(cl)

    # if any(isinstance(a.type, str) for a in attrs):
    #     # PEP 563 annotations - need to be resolved.
    #     resolve_types(cl)

    lines.append(f"def {fn_name}(o, *_):")
    lines.append("  res = {")
    for a in attrs:
        an = a.name
        override = kwargs.pop(an, _neutral)
        type = a.type
        if isinstance(type, TypeVar):
            type = getattr(mapping, type.__name__, type)

        kn = (
            an
            if getattr(override, "rename", None) is None
            else override.rename
        )
        globs[f"__c_t_{an}"] = type
        if (
            a.default is dataclasses.MISSING
            and a.default_factory is dataclasses.MISSING
        ):
            lines.append(f"    '{an}': __c_s(o['{kn}'], __c_t_{an}),")
        else:
            post_lines.append(f"  if '{kn}' in o:")
            post_lines.append(
                f"    res['{an}'] = __c_s(o['{kn}'], __c_t_{an})"
            )
    lines.append("    }")

    total_lines = lines + post_lines + ["  return __cl(**res)"]

    eval(compile("\n".join(total_lines), "", "exec"), globs)

    return globs[fn_name]
