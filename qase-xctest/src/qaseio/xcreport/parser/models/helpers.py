from typing import List, Type, TypeVar

T = TypeVar("T")
_subtypes = []


def try_from_report(try_block, params):
    try:
        return try_block()
    except Exception:
        if "default" in params:
            return params["default"]
        else:
            raise


def registry_subtype(child_type: Type[T], parent_type: Type[T]):
    _subtypes.append((child_type, parent_type))


def list_from_report(to_type: Type[T], report, params={}) -> List[T]:

    childs = []
    for (child_type, parent_type) in _subtypes:
        if parent_type == to_type:
            childs.append(child_type)

    if childs:
        return __list_object_from_array(childs, to_type, report, params)

    def convert():
        if report["_type"]["_name"] != "Array":
            raise ValueError("type error")

        actions = []
        for item in report["_values"]:
            actions.append(to_type.from_report(item))

        return actions

    return try_from_report(convert, params)


def __list_object_from_array(
    to_types: [], abstract_type: Type[T], report, params={}
) -> List[T]:
    def convert():
        if report["_type"]["_name"] != "Array":
            raise ValueError("type error")

        actions = []
        for item in report["_values"]:
            item_obj = None
            for to_type in to_types:
                try:
                    item_obj = to_type.from_report(item)
                except ValueError:
                    continue
                if item_obj is not None:
                    break

            if item_obj is not None and isinstance(item_obj, abstract_type):
                actions.append(item_obj)
            else:
                raise ValueError("type error")

        return actions

    return try_from_report(convert, params)


def enum_from_report(to_type: Type[T], report, params={}) -> T:
    def convert():
        if report["_type"]["_name"] != "String":
            raise ValueError("type error")

        return to_type(report["_value"])

    return try_from_report(convert, params)


def float_from_report(report, params={}) -> float:
    def convert():
        if report["_type"]["_name"] != "Double":
            raise ValueError("type error")

        return float(report["_value"])

    return try_from_report(convert, params)


def string_from_report(report, params={}) -> str:
    def convert():
        if report["_type"]["_name"] != "String":
            raise ValueError("type error")

        return report["_value"]

    return try_from_report(convert, params)


def object_from_report(to_type: Type[T], report, params={}):
    def convert():
        return to_type.from_report(report)

    return try_from_report(convert, params)
