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
from pydantic import Field
from qaseio.models.custom_field_value import CustomFieldValue
from qaseio.models.run_environment import RunEnvironment
from qaseio.models.run_milestone import RunMilestone
from qaseio.models.run_stats import RunStats
from qaseio.models.tag_value import TagValue
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class Run(BaseModel):
    """
    Run
    """ # noqa: E501
    id: Optional[StrictInt] = None
    title: Optional[StrictStr] = None
    description: Optional[StrictStr] = None
    status: Optional[StrictInt] = None
    status_text: Optional[StrictStr] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    public: Optional[StrictBool] = None
    stats: Optional[RunStats] = None
    time_spent: Optional[StrictInt] = Field(default=None, description="Time in ms.")
    environment: Optional[RunEnvironment] = None
    milestone: Optional[RunMilestone] = None
    custom_fields: Optional[List[CustomFieldValue]] = None
    tags: Optional[List[TagValue]] = None
    cases: Optional[List[StrictInt]] = None
    __properties: ClassVar[List[str]] = ["id", "title", "description", "status", "status_text", "start_time", "end_time", "public", "stats", "time_spent", "environment", "milestone", "custom_fields", "tags", "cases"]

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
        """Create an instance of Run from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of stats
        if self.stats:
            _dict['stats'] = self.stats.to_dict()
        # override the default output from pydantic by calling `to_dict()` of environment
        if self.environment:
            _dict['environment'] = self.environment.to_dict()
        # override the default output from pydantic by calling `to_dict()` of milestone
        if self.milestone:
            _dict['milestone'] = self.milestone.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in custom_fields (list)
        _items = []
        if self.custom_fields:
            for _item in self.custom_fields:
                if _item:
                    _items.append(_item.to_dict())
            _dict['custom_fields'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in tags (list)
        _items = []
        if self.tags:
            for _item in self.tags:
                if _item:
                    _items.append(_item.to_dict())
            _dict['tags'] = _items
        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict['description'] = None

        # set to None if start_time (nullable) is None
        # and model_fields_set contains the field
        if self.start_time is None and "start_time" in self.model_fields_set:
            _dict['start_time'] = None

        # set to None if end_time (nullable) is None
        # and model_fields_set contains the field
        if self.end_time is None and "end_time" in self.model_fields_set:
            _dict['end_time'] = None

        # set to None if environment (nullable) is None
        # and model_fields_set contains the field
        if self.environment is None and "environment" in self.model_fields_set:
            _dict['environment'] = None

        # set to None if milestone (nullable) is None
        # and model_fields_set contains the field
        if self.milestone is None and "milestone" in self.model_fields_set:
            _dict['milestone'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of Run from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "title": obj.get("title"),
            "description": obj.get("description"),
            "status": obj.get("status"),
            "status_text": obj.get("status_text"),
            "start_time": obj.get("start_time"),
            "end_time": obj.get("end_time"),
            "public": obj.get("public"),
            "stats": RunStats.from_dict(obj.get("stats")) if obj.get("stats") is not None else None,
            "time_spent": obj.get("time_spent"),
            "environment": RunEnvironment.from_dict(obj.get("environment")) if obj.get("environment") is not None else None,
            "milestone": RunMilestone.from_dict(obj.get("milestone")) if obj.get("milestone") is not None else None,
            "custom_fields": [CustomFieldValue.from_dict(_item) for _item in obj.get("custom_fields")] if obj.get("custom_fields") is not None else None,
            "tags": [TagValue.from_dict(_item) for _item in obj.get("tags")] if obj.get("tags") is not None else None,
            "cases": obj.get("cases")
        })
        return _obj


