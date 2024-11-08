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

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from typing import Optional, Set
from typing_extensions import Self

class ProjectCreate(BaseModel):
    """
    ProjectCreate
    """ # noqa: E501
    title: StrictStr = Field(description="Project title.")
    code: Annotated[str, Field(strict=True)] = Field(description="Project code. Unique for team. Digits and special characters are not allowed.")
    description: Optional[StrictStr] = Field(default=None, description="Project description.")
    access: Optional[StrictStr] = None
    group: Optional[StrictStr] = Field(default=None, description="Team group hash. Required if access param is set to group.")
    settings: Optional[Dict[str, Any]] = Field(default=None, description="Additional project settings.")
    __properties: ClassVar[List[str]] = ["title", "code", "description", "access", "group", "settings"]

    @field_validator('code')
    def code_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[a-zA-Z]{2,10}$", value):
            raise ValueError(r"must validate the regular expression /^[a-zA-Z]{2,10}$/")
        return value

    @field_validator('access')
    def access_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['all', 'group', 'none']):
            raise ValueError("must be one of enum values ('all', 'group', 'none')")
        return value

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
        """Create an instance of ProjectCreate from a JSON string"""
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
        """Create an instance of ProjectCreate from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "title": obj.get("title"),
            "code": obj.get("code"),
            "description": obj.get("description"),
            "access": obj.get("access"),
            "group": obj.get("group"),
            "settings": obj.get("settings")
        })
        return _obj

