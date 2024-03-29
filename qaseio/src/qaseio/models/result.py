# coding: utf-8

"""
    Qase.io TestOps API

    Qase TestOps API Specification.

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
from typing import Any, ClassVar, Dict, List, Optional
from pydantic import BaseModel, StrictBool, StrictInt, StrictStr
from qaseio.models.attachment import Attachment
from qaseio.models.test_step_result import TestStepResult
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class Result(BaseModel):
    """
    Result
    """ # noqa: E501
    hash: Optional[StrictStr] = None
    comment: Optional[StrictStr] = None
    stacktrace: Optional[StrictStr] = None
    run_id: Optional[StrictInt] = None
    case_id: Optional[StrictInt] = None
    steps: Optional[List[TestStepResult]] = None
    status: Optional[StrictStr] = None
    is_api_result: Optional[StrictBool] = None
    time_spent_ms: Optional[StrictInt] = None
    end_time: Optional[datetime] = None
    attachments: Optional[List[Attachment]] = None
    __properties: ClassVar[List[str]] = ["hash", "comment", "stacktrace", "run_id", "case_id", "steps", "status", "is_api_result", "time_spent_ms", "end_time", "attachments"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of Result from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in steps (list)
        _items = []
        if self.steps:
            for _item in self.steps:
                if _item:
                    _items.append(_item.to_dict())
            _dict['steps'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in attachments (list)
        _items = []
        if self.attachments:
            for _item in self.attachments:
                if _item:
                    _items.append(_item.to_dict())
            _dict['attachments'] = _items
        # set to None if comment (nullable) is None
        # and model_fields_set contains the field
        if self.comment is None and "comment" in self.model_fields_set:
            _dict['comment'] = None

        # set to None if stacktrace (nullable) is None
        # and model_fields_set contains the field
        if self.stacktrace is None and "stacktrace" in self.model_fields_set:
            _dict['stacktrace'] = None

        # set to None if steps (nullable) is None
        # and model_fields_set contains the field
        if self.steps is None and "steps" in self.model_fields_set:
            _dict['steps'] = None

        # set to None if end_time (nullable) is None
        # and model_fields_set contains the field
        if self.end_time is None and "end_time" in self.model_fields_set:
            _dict['end_time'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of Result from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "hash": obj.get("hash"),
            "comment": obj.get("comment"),
            "stacktrace": obj.get("stacktrace"),
            "run_id": obj.get("run_id"),
            "case_id": obj.get("case_id"),
            "steps": [TestStepResult.from_dict(_item) for _item in obj.get("steps")] if obj.get("steps") is not None else None,
            "status": obj.get("status"),
            "is_api_result": obj.get("is_api_result"),
            "time_spent_ms": obj.get("time_spent_ms"),
            "end_time": obj.get("end_time"),
            "attachments": [Attachment.from_dict(_item) for _item in obj.get("attachments")] if obj.get("attachments") is not None else None
        })
        return _obj


