import sys
from typing import List, MutableSequence, Sequence, Tuple

version_info = sys.version_info[0:3]
is_py37 = version_info[:2] == (3, 7)
is_py38 = version_info[:2] == (3, 8)


def is_attrs_class(cls):
    return getattr(cls, "__attrs_attrs__", None) is not None


def has_args(cls):
    return getattr(cls, "__args__", None) is not None


def _subclass(typ):
    """ a shortcut """
    return lambda cls: issubclass(cls, typ)


if is_py37 or is_py38:
    from typing import Union, _GenericAlias

    def is_tuple(type):
        return type is Tuple or (
            type.__class__ is _GenericAlias
            and issubclass(type.__origin__, Tuple)
        )

    def is_union_type(obj):
        return (
            obj is Union
            or isinstance(obj, _GenericAlias)
            and obj.__origin__ is Union
        )

    def is_sequence(type):
        return type is List or (
            type.__class__ is _GenericAlias
            and type.__origin__ is not Union
            and issubclass(type.__origin__, Sequence)
        )


else:
    # 3.9+
    from typing import (
        Union,
        _GenericAlias,
        _UnionGenericAlias,
    )

    def is_tuple(type):
        return (
            type in (Tuple, tuple)
            or (
                type.__class__ is _GenericAlias
                and issubclass(type.__origin__, Tuple)
            )
            or (getattr(type, "__origin__", None) is tuple)
        )

    def is_union_type(obj):
        return (
            obj is Union
            or isinstance(obj, _UnionGenericAlias)
            and obj.__origin__ is Union
        )

    def is_sequence(type):
        return (
            type in (List, list, Sequence, MutableSequence)
            or (
                type.__class__ is _GenericAlias
                and issubclass(type.__origin__, Sequence)
            )
            or (getattr(type, "__origin__", None) is list)
        )
