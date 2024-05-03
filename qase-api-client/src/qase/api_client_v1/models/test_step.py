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

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from src.qase.api_client_v1.models.attachment import Attachment
from typing import Optional, Set
from typing_extensions import Self

class TestStep(BaseModel):
    """
    TestStep
    """ # noqa: E501
    hash: Optional[StrictStr] = None
    shared_step_hash: Optional[StrictStr] = None
    shared_step_nested_hash: Optional[StrictStr] = None
    position: Optional[StrictInt] = None
    action: Optional[StrictStr] = None
    expected_result: Optional[StrictStr] = None
    data: Optional[StrictStr] = None
    attachments: Optional[List[Attachment]] = None
    steps: Optional[List[Dict[str, Any]]] = Field(default=None, description="Nested steps will be here. The same structure is used for them.")
    __properties: ClassVar[List[str]] = ["hash", "shared_step_hash", "shared_step_nested_hash", "position", "action", "expected_result", "data", "attachments", "steps"]

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
        """Create an instance of TestStep from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in attachments (list)
        _items = []
        if self.attachments:
            for _item in self.attachments:
                if _item:
                    _items.append(_item.to_dict())
            _dict['attachments'] = _items
        # set to None if shared_step_hash (nullable) is None
        # and model_fields_set contains the field
        if self.shared_step_hash is None and "shared_step_hash" in self.model_fields_set:
            _dict['shared_step_hash'] = None

        # set to None if shared_step_nested_hash (nullable) is None
        # and model_fields_set contains the field
        if self.shared_step_nested_hash is None and "shared_step_nested_hash" in self.model_fields_set:
            _dict['shared_step_nested_hash'] = None

        # set to None if expected_result (nullable) is None
        # and model_fields_set contains the field
        if self.expected_result is None and "expected_result" in self.model_fields_set:
            _dict['expected_result'] = None

        # set to None if data (nullable) is None
        # and model_fields_set contains the field
        if self.data is None and "data" in self.model_fields_set:
            _dict['data'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TestStep from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "hash": obj.get("hash"),
            "shared_step_hash": obj.get("shared_step_hash"),
            "shared_step_nested_hash": obj.get("shared_step_nested_hash"),
            "position": obj.get("position"),
            "action": obj.get("action"),
            "expected_result": obj.get("expected_result"),
            "data": obj.get("data"),
            "attachments": [Attachment.from_dict(_item) for _item in obj["attachments"]] if obj.get("attachments") is not None else None,
            "steps": obj.get("steps")
        })
        return _obj

