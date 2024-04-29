# coding: utf-8

"""
    Qase.io TestOps API v2

    Qase TestOps API v2 Specification.

    The version of the OpenAPI document: 2.0.0
    Contact: support@qase.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Union
from .result_execution import ResultExecution
from .result_relations import ResultRelations
from .result_step import ResultStep
from .result_steps_type import ResultStepsType
from typing import Optional, Set
from typing_extensions import Self

class ResultCreate(BaseModel):
    """
    ResultCreate
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="If passed, used as an idempotency key")
    title: StrictStr
    signature: Optional[StrictStr] = None
    testops_id: Optional[StrictInt] = None
    execution: ResultExecution
    fields: Optional[Dict[str, StrictStr]] = None
    attachments: Optional[List[StrictStr]] = None
    steps: Optional[List[ResultStep]] = None
    steps_type: Optional[ResultStepsType] = None
    params: Optional[Dict[str, StrictStr]] = None
    author: Optional[StrictStr] = None
    relations: Optional[ResultRelations] = None
    muted: Optional[StrictBool] = None
    message: Optional[StrictStr] = None
    created_at: Optional[Union[StrictFloat, StrictInt]] = None
    __properties: ClassVar[List[str]] = ["id", "title", "signature", "testops_id", "execution", "fields", "attachments", "steps", "steps_type", "params", "author", "relations", "muted", "message", "created_at"]

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
        """Create an instance of ResultCreate from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of execution
        if self.execution:
            _dict['execution'] = self.execution.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in steps (list)
        _items = []
        if self.steps:
            for _item in self.steps:
                if _item:
                    _items.append(_item.to_dict())
            _dict['steps'] = _items
        # override the default output from pydantic by calling `to_dict()` of relations
        if self.relations:
            _dict['relations'] = self.relations.to_dict()
        # set to None if testops_id (nullable) is None
        # and model_fields_set contains the field
        if self.testops_id is None and "testops_id" in self.model_fields_set:
            _dict['testops_id'] = None

        # set to None if steps_type (nullable) is None
        # and model_fields_set contains the field
        if self.steps_type is None and "steps_type" in self.model_fields_set:
            _dict['steps_type'] = None

        # set to None if relations (nullable) is None
        # and model_fields_set contains the field
        if self.relations is None and "relations" in self.model_fields_set:
            _dict['relations'] = None

        # set to None if message (nullable) is None
        # and model_fields_set contains the field
        if self.message is None and "message" in self.model_fields_set:
            _dict['message'] = None

        # set to None if created_at (nullable) is None
        # and model_fields_set contains the field
        if self.created_at is None and "created_at" in self.model_fields_set:
            _dict['created_at'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ResultCreate from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "title": obj.get("title"),
            "signature": obj.get("signature"),
            "testops_id": obj.get("testops_id"),
            "execution": ResultExecution.from_dict(obj["execution"]) if obj.get("execution") is not None else None,
            "fields": obj.get("fields"),
            "attachments": obj.get("attachments"),
            "steps": [ResultStep.from_dict(_item) for _item in obj["steps"]] if obj.get("steps") is not None else None,
            "steps_type": obj.get("steps_type"),
            "params": obj.get("params"),
            "author": obj.get("author"),
            "relations": ResultRelations.from_dict(obj["relations"]) if obj.get("relations") is not None else None,
            "muted": obj.get("muted"),
            "message": obj.get("message"),
            "created_at": obj.get("created_at")
        })
        return _obj


