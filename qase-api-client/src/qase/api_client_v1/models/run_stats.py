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

from pydantic import BaseModel, ConfigDict, StrictInt
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class RunStats(BaseModel):
    """
    RunStats
    """ # noqa: E501
    total: Optional[StrictInt] = None
    statuses: Optional[Dict[str, StrictInt]] = None
    untested: Optional[StrictInt] = None
    passed: Optional[StrictInt] = None
    failed: Optional[StrictInt] = None
    blocked: Optional[StrictInt] = None
    skipped: Optional[StrictInt] = None
    retest: Optional[StrictInt] = None
    in_progress: Optional[StrictInt] = None
    invalid: Optional[StrictInt] = None
    __properties: ClassVar[List[str]] = ["total", "statuses", "untested", "passed", "failed", "blocked", "skipped", "retest", "in_progress", "invalid"]

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
        """Create an instance of RunStats from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RunStats from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "total": obj.get("total"),
            "statuses": obj.get("statuses"),
            "untested": obj.get("untested"),
            "passed": obj.get("passed"),
            "failed": obj.get("failed"),
            "blocked": obj.get("blocked"),
            "skipped": obj.get("skipped"),
            "retest": obj.get("retest"),
            "in_progress": obj.get("in_progress"),
            "invalid": obj.get("invalid")
        })
        return _obj

