# coding: utf-8

"""
    Qase.io TestOps API v1

    Qase TestOps API v1 Specification.

    The version of the OpenAPI document: 1.0.0
    Contact: support@qase.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from qase.api_client_v1.models.attachment import Attachment
from qase.api_client_v1.models.custom_field_value import CustomFieldValue
from qase.api_client_v1.models.tag_value import TagValue
from typing import Optional, Set
from typing_extensions import Self

class Defect(BaseModel):
    """
    Defect
    """ # noqa: E501
    id: Optional[StrictInt] = None
    title: Optional[StrictStr] = None
    actual_result: Optional[StrictStr] = None
    severity: Optional[StrictStr] = None
    status: Optional[StrictStr] = None
    milestone_id: Optional[StrictInt] = None
    custom_fields: Optional[List[CustomFieldValue]] = None
    attachments: Optional[List[Attachment]] = None
    resolved_at: Optional[datetime] = None
    member_id: Optional[StrictInt] = Field(default=None, description="Deprecated, use `author_id` instead.")
    author_id: Optional[StrictInt] = None
    external_data: Optional[StrictStr] = None
    runs: Optional[List[StrictInt]] = None
    results: Optional[List[StrictStr]] = None
    tags: Optional[List[TagValue]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created: Optional[StrictStr] = Field(default=None, description="Deprecated, use the `created_at` property instead.")
    updated: Optional[StrictStr] = Field(default=None, description="Deprecated, use the `updated_at` property instead.")
    __properties: ClassVar[List[str]] = ["id", "title", "actual_result", "severity", "status", "milestone_id", "custom_fields", "attachments", "resolved_at", "member_id", "author_id", "external_data", "runs", "results", "tags", "created_at", "updated_at", "created", "updated"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of Defect from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in custom_fields (list)
        _items = []
        if self.custom_fields:
            for _item in self.custom_fields:
                if _item:
                    _items.append(_item.to_dict())
            _dict['custom_fields'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in attachments (list)
        _items = []
        if self.attachments:
            for _item in self.attachments:
                if _item:
                    _items.append(_item.to_dict())
            _dict['attachments'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in tags (list)
        _items = []
        if self.tags:
            for _item in self.tags:
                if _item:
                    _items.append(_item.to_dict())
            _dict['tags'] = _items
        # set to None if milestone_id (nullable) is None
        # and model_fields_set contains the field
        if self.milestone_id is None and "milestone_id" in self.model_fields_set:
            _dict['milestone_id'] = None

        # set to None if resolved_at (nullable) is None
        # and model_fields_set contains the field
        if self.resolved_at is None and "resolved_at" in self.model_fields_set:
            _dict['resolved_at'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Defect from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "title": obj.get("title"),
            "actual_result": obj.get("actual_result"),
            "severity": obj.get("severity"),
            "status": obj.get("status"),
            "milestone_id": obj.get("milestone_id"),
            "custom_fields": [CustomFieldValue.from_dict(_item) for _item in obj["custom_fields"]] if obj.get("custom_fields") is not None else None,
            "attachments": [Attachment.from_dict(_item) for _item in obj["attachments"]] if obj.get("attachments") is not None else None,
            "resolved_at": obj.get("resolved_at"),
            "member_id": obj.get("member_id"),
            "author_id": obj.get("author_id"),
            "external_data": obj.get("external_data"),
            "runs": obj.get("runs"),
            "results": obj.get("results"),
            "tags": [TagValue.from_dict(_item) for _item in obj["tags"]] if obj.get("tags") is not None else None,
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "created": obj.get("created"),
            "updated": obj.get("updated")
        })
        return _obj


