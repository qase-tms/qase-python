import types
from dataclasses import _EMPTY_METADATA, Field, dataclass
from dataclasses import field as fld
from enum import Enum

_pref = "convclasses"


class Mods(Enum):
    name = f"{_pref}_modify_name"


@dataclass
class _Modificator:
    field: Field

    @property
    def obj_name(self):
        if self.field.metadata.get(Mods.name):
            modifier = self.field.metadata.get(Mods.name)
            if modifier.get("from"):
                return modifier.get("from")
        return self.field.name


class _Modifiers:
    @staticmethod
    def name(name: str, field: Field = None):
        if field is None:
            field = fld()
        meta = dict(getattr(field, "metadata", _EMPTY_METADATA))
        meta[Mods.name] = {"from": name}
        field.metadata = types.MappingProxyType(meta)
        return field


mod = _Modifiers
