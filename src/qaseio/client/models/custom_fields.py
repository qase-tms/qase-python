from typing import List

import attr

from qaseio.client.models.base import DefaultList


@attr.s
class CustomFieldInfo:
    id = attr.ib(default=None)
    title = attr.ib(default=None)
    type = attr.ib(default=None)
    placeholder = attr.ib(default=None)
    default_value = attr.ib(default=None)
    value = attr.ib(default=None)
    is_required: bool = attr.ib(default=None)
    is_visible: bool = attr.ib(default=None)
    is_filterable: bool = attr.ib(default=None)
    created = attr.ib(default=None)
    updated = attr.ib(default=None)


@attr.s
class CustomFieldList(DefaultList):
    entities: List[CustomFieldInfo] = attr.ib(factory=list)
