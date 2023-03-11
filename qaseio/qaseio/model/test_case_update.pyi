# coding: utf-8

"""
    Qase.io API

    Qase API Specification.  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: support@qase.io
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from qaseio import schemas  # noqa: F401


class TestCaseUpdate(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
            description = schemas.StrSchema
            preconditions = schemas.StrSchema
            postconditions = schemas.StrSchema
            
            
            class title(
                schemas.StrSchema
            ):
                pass
            severity = schemas.IntSchema
            priority = schemas.IntSchema
            behavior = schemas.IntSchema
            type = schemas.IntSchema
            layer = schemas.IntSchema
            is_flaky = schemas.IntSchema
            suite_id = schemas.Int64Schema
            milestone_id = schemas.Int64Schema
            automation = schemas.IntSchema
            status = schemas.IntSchema
        
            @staticmethod
            def attachments() -> typing.Type['AttachmentHashList']:
                return AttachmentHashList
            
            
            class steps(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['TestStepCreate']:
                        return TestStepCreate
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['TestStepCreate'], typing.List['TestStepCreate']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'steps':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'TestStepCreate':
                    return super().__getitem__(i)
            
            
            class tags(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    items = schemas.StrSchema
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'tags':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> MetaOapg.items:
                    return super().__getitem__(i)
            
            
            class params(
                schemas.DictBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneFrozenDictMixin
            ):
            
            
                class MetaOapg:
                    
                    
                    class additional_properties(
                        schemas.ListSchema
                    ):
                    
                    
                        class MetaOapg:
                            items = schemas.StrSchema
                    
                        def __new__(
                            cls,
                            _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                            _configuration: typing.Optional[schemas.Configuration] = None,
                        ) -> 'additional_properties':
                            return super().__new__(
                                cls,
                                _arg,
                                _configuration=_configuration,
                            )
                    
                        def __getitem__(self, i: int) -> MetaOapg.items:
                            return super().__getitem__(i)
            
                
                def __getitem__(self, name: typing.Union[str, ]) -> MetaOapg.additional_properties:
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                def get_item_oapg(self, name: typing.Union[str, ]) -> MetaOapg.additional_properties:
                    return super().get_item_oapg(name)
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, None, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[MetaOapg.additional_properties, list, tuple, ],
                ) -> 'params':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class custom_field(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    additional_properties = schemas.StrSchema
                
                def __getitem__(self, name: typing.Union[str, ]) -> MetaOapg.additional_properties:
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                def get_item_oapg(self, name: typing.Union[str, ]) -> MetaOapg.additional_properties:
                    return super().get_item_oapg(name)
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[MetaOapg.additional_properties, str, ],
                ) -> 'custom_field':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            __annotations__ = {
                "description": description,
                "preconditions": preconditions,
                "postconditions": postconditions,
                "title": title,
                "severity": severity,
                "priority": priority,
                "behavior": behavior,
                "type": type,
                "layer": layer,
                "is_flaky": is_flaky,
                "suite_id": suite_id,
                "milestone_id": milestone_id,
                "automation": automation,
                "status": status,
                "attachments": attachments,
                "steps": steps,
                "tags": tags,
                "params": params,
                "custom_field": custom_field,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["preconditions"]) -> MetaOapg.properties.preconditions: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["postconditions"]) -> MetaOapg.properties.postconditions: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["title"]) -> MetaOapg.properties.title: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["severity"]) -> MetaOapg.properties.severity: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["priority"]) -> MetaOapg.properties.priority: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["behavior"]) -> MetaOapg.properties.behavior: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["layer"]) -> MetaOapg.properties.layer: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["is_flaky"]) -> MetaOapg.properties.is_flaky: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["suite_id"]) -> MetaOapg.properties.suite_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["milestone_id"]) -> MetaOapg.properties.milestone_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["automation"]) -> MetaOapg.properties.automation: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["attachments"]) -> 'AttachmentHashList': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["steps"]) -> MetaOapg.properties.steps: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["tags"]) -> MetaOapg.properties.tags: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["params"]) -> MetaOapg.properties.params: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["custom_field"]) -> MetaOapg.properties.custom_field: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["description", "preconditions", "postconditions", "title", "severity", "priority", "behavior", "type", "layer", "is_flaky", "suite_id", "milestone_id", "automation", "status", "attachments", "steps", "tags", "params", "custom_field", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["description"]) -> typing.Union[MetaOapg.properties.description, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["preconditions"]) -> typing.Union[MetaOapg.properties.preconditions, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["postconditions"]) -> typing.Union[MetaOapg.properties.postconditions, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["title"]) -> typing.Union[MetaOapg.properties.title, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["severity"]) -> typing.Union[MetaOapg.properties.severity, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["priority"]) -> typing.Union[MetaOapg.properties.priority, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["behavior"]) -> typing.Union[MetaOapg.properties.behavior, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["type"]) -> typing.Union[MetaOapg.properties.type, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["layer"]) -> typing.Union[MetaOapg.properties.layer, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["is_flaky"]) -> typing.Union[MetaOapg.properties.is_flaky, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["suite_id"]) -> typing.Union[MetaOapg.properties.suite_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["milestone_id"]) -> typing.Union[MetaOapg.properties.milestone_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["automation"]) -> typing.Union[MetaOapg.properties.automation, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> typing.Union[MetaOapg.properties.status, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["attachments"]) -> typing.Union['AttachmentHashList', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["steps"]) -> typing.Union[MetaOapg.properties.steps, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["tags"]) -> typing.Union[MetaOapg.properties.tags, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["params"]) -> typing.Union[MetaOapg.properties.params, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["custom_field"]) -> typing.Union[MetaOapg.properties.custom_field, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["description", "preconditions", "postconditions", "title", "severity", "priority", "behavior", "type", "layer", "is_flaky", "suite_id", "milestone_id", "automation", "status", "attachments", "steps", "tags", "params", "custom_field", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        description: typing.Union[MetaOapg.properties.description, str, schemas.Unset] = schemas.unset,
        preconditions: typing.Union[MetaOapg.properties.preconditions, str, schemas.Unset] = schemas.unset,
        postconditions: typing.Union[MetaOapg.properties.postconditions, str, schemas.Unset] = schemas.unset,
        title: typing.Union[MetaOapg.properties.title, str, schemas.Unset] = schemas.unset,
        severity: typing.Union[MetaOapg.properties.severity, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        priority: typing.Union[MetaOapg.properties.priority, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        behavior: typing.Union[MetaOapg.properties.behavior, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        type: typing.Union[MetaOapg.properties.type, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        layer: typing.Union[MetaOapg.properties.layer, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        is_flaky: typing.Union[MetaOapg.properties.is_flaky, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        suite_id: typing.Union[MetaOapg.properties.suite_id, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        milestone_id: typing.Union[MetaOapg.properties.milestone_id, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        automation: typing.Union[MetaOapg.properties.automation, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        status: typing.Union[MetaOapg.properties.status, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        attachments: typing.Union['AttachmentHashList', schemas.Unset] = schemas.unset,
        steps: typing.Union[MetaOapg.properties.steps, list, tuple, schemas.Unset] = schemas.unset,
        tags: typing.Union[MetaOapg.properties.tags, list, tuple, schemas.Unset] = schemas.unset,
        params: typing.Union[MetaOapg.properties.params, dict, frozendict.frozendict, None, schemas.Unset] = schemas.unset,
        custom_field: typing.Union[MetaOapg.properties.custom_field, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'TestCaseUpdate':
        return super().__new__(
            cls,
            *_args,
            description=description,
            preconditions=preconditions,
            postconditions=postconditions,
            title=title,
            severity=severity,
            priority=priority,
            behavior=behavior,
            type=type,
            layer=layer,
            is_flaky=is_flaky,
            suite_id=suite_id,
            milestone_id=milestone_id,
            automation=automation,
            status=status,
            attachments=attachments,
            steps=steps,
            tags=tags,
            params=params,
            custom_field=custom_field,
            _configuration=_configuration,
            **kwargs,
        )

from qaseio.model.attachment_hash_list import AttachmentHashList
from qaseio.model.test_step_create import TestStepCreate
