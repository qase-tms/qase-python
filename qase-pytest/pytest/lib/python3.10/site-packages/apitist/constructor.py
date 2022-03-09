from dataclasses import MISSING
from enum import Enum

import attr
import cattr
import convclasses
import pendulum

from apitist.utils import _subclass


def _structure_date_time(isostring, _):
    """Structure hook for :class:`pendulum.DateTime`"""
    if isinstance(isostring, str):
        return pendulum.parse(isostring)
    else:
        return None


def _unstructure_date_time(dt):
    """Unstructure hook for :class:`pendulum.DateTime`"""
    if isinstance(dt, pendulum.DateTime):
        return dt.to_rfc3339_string()
    else:
        return None


class ConverterType(Enum):
    ATTRS = "attrs"
    DATACLASS = "dataclass"


class _Converter:
    """Converts between structured and unstructured data."""

    def set_dict_factory(self, dict_factory):
        self._dict_factory = dict_factory

    def register_hooks(self, cls, structure, unstructure):
        """
        Register primitive-to-class and class-to-primitive converter
        functions for a class.

        The structure function should take two arguments:
          * a Python object to be converted,
          * the type to convert to

        and return the instance of the class. The type may seem redundant, but
        is sometimes needed (for example, when dealing with generic classes).

        The unstructure function should take an instance of the class and
        return its Python equivalent.

        """
        self.register_structure_hook(cls, structure)
        self.register_unstructure_hook(cls, unstructure)

    def register_hooks_funcs(self, check_func, structure, unstructure):
        """
        Register primitive-to-class and class-to-primitive converter functions
        for a class, using a function to check if it's a match.
        """
        self.register_structure_hook_func(check_func, structure)
        self.register_unstructure_hook_func(check_func, unstructure)

    def register_additional_hooks(self):
        """
        Register additional hooks:

        * :class:`str` - all its instances would be structured
          and unstructured as :class:`str`
        * :class:`pendulum.DateTime` - datetime would be parsed using pendulum
          and unstructured in RFC3339 format
        """
        self.register_hooks_funcs(
            _subclass(str), self._unstructure_identity, self._structure_call
        )
        self.register_hooks(
            pendulum.DateTime, _structure_date_time, _unstructure_date_time
        )

    def _structure_call(self, obj, cl):
        """Just call ``cl`` with the given ``obj``."""
        if obj is None:
            return None
        return cl(obj)


class NothingDict(dict):
    """
    Default dict for unstructuring

    It is used for unstructuring Type with ignoring some fields.
    If given field is :class:`attr.NOTHING` - it would not be unstructured in
    dict.
    """

    def __setitem__(self, key, value):
        if value == attr.NOTHING:
            return
        super().__setitem__(key, value)


class MissingDict(dict):
    """
    Default dict for unstructuring

    It is used for unstructuring Type with ignoring some fields.
    If given field is :class:`dataclasses.MISSING` -
    it would not be unstructured in dict.
    """

    def __setitem__(self, key, value):
        if value == MISSING:
            return
        super().__setitem__(key, value)


class AttrsConverter(_Converter, cattr.Converter):
    _converter_type = ConverterType.ATTRS

    def __init__(self):
        super().__init__()
        self.set_dict_factory(NothingDict)


class DataclassConverter(_Converter, convclasses.Converter):
    _converter_type = ConverterType.DATACLASS

    def __init__(self):
        super().__init__()
        self.set_dict_factory(MissingDict)


def Converter(converter_type: ConverterType = ConverterType.ATTRS):
    if converter_type == ConverterType.ATTRS:
        return AttrsConverter()
    else:
        return DataclassConverter()


converter = Converter()
converter.register_additional_hooks()

convclass = Converter(ConverterType.DATACLASS)
convclass.register_additional_hooks()
