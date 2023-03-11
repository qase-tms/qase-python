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


class RunCreate(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "title",
        }
        
        class properties:
            
            
            class title(
                schemas.StrSchema
            ):
                pass
            
            
            class description(
                schemas.StrSchema
            ):
                pass
            include_all_cases = schemas.BoolSchema
            
            
            class cases(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    items = schemas.Int64Schema
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, decimal.Decimal, int, ]], typing.List[typing.Union[MetaOapg.items, decimal.Decimal, int, ]]],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'cases':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> MetaOapg.items:
                    return super().__getitem__(i)
            is_autotest = schemas.BoolSchema
            
            
            class environment_id(
                schemas.Int64Schema
            ):
                pass
            
            
            class milestone_id(
                schemas.Int64Schema
            ):
                pass
            
            
            class plan_id(
                schemas.Int64Schema
            ):
                pass
            
            
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
                "title": title,
                "description": description,
                "include_all_cases": include_all_cases,
                "cases": cases,
                "is_autotest": is_autotest,
                "environment_id": environment_id,
                "milestone_id": milestone_id,
                "plan_id": plan_id,
                "tags": tags,
                "custom_field": custom_field,
            }
    
    title: MetaOapg.properties.title
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["title"]) -> MetaOapg.properties.title: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["include_all_cases"]) -> MetaOapg.properties.include_all_cases: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["cases"]) -> MetaOapg.properties.cases: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["is_autotest"]) -> MetaOapg.properties.is_autotest: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["environment_id"]) -> MetaOapg.properties.environment_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["milestone_id"]) -> MetaOapg.properties.milestone_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["plan_id"]) -> MetaOapg.properties.plan_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["tags"]) -> MetaOapg.properties.tags: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["custom_field"]) -> MetaOapg.properties.custom_field: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["title", "description", "include_all_cases", "cases", "is_autotest", "environment_id", "milestone_id", "plan_id", "tags", "custom_field", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["title"]) -> MetaOapg.properties.title: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["description"]) -> typing.Union[MetaOapg.properties.description, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["include_all_cases"]) -> typing.Union[MetaOapg.properties.include_all_cases, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["cases"]) -> typing.Union[MetaOapg.properties.cases, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["is_autotest"]) -> typing.Union[MetaOapg.properties.is_autotest, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["environment_id"]) -> typing.Union[MetaOapg.properties.environment_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["milestone_id"]) -> typing.Union[MetaOapg.properties.milestone_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["plan_id"]) -> typing.Union[MetaOapg.properties.plan_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["tags"]) -> typing.Union[MetaOapg.properties.tags, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["custom_field"]) -> typing.Union[MetaOapg.properties.custom_field, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["title", "description", "include_all_cases", "cases", "is_autotest", "environment_id", "milestone_id", "plan_id", "tags", "custom_field", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        title: typing.Union[MetaOapg.properties.title, str, ],
        description: typing.Union[MetaOapg.properties.description, str, schemas.Unset] = schemas.unset,
        include_all_cases: typing.Union[MetaOapg.properties.include_all_cases, bool, schemas.Unset] = schemas.unset,
        cases: typing.Union[MetaOapg.properties.cases, list, tuple, schemas.Unset] = schemas.unset,
        is_autotest: typing.Union[MetaOapg.properties.is_autotest, bool, schemas.Unset] = schemas.unset,
        environment_id: typing.Union[MetaOapg.properties.environment_id, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        milestone_id: typing.Union[MetaOapg.properties.milestone_id, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        plan_id: typing.Union[MetaOapg.properties.plan_id, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        tags: typing.Union[MetaOapg.properties.tags, list, tuple, schemas.Unset] = schemas.unset,
        custom_field: typing.Union[MetaOapg.properties.custom_field, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'RunCreate':
        return super().__new__(
            cls,
            *_args,
            title=title,
            description=description,
            include_all_cases=include_all_cases,
            cases=cases,
            is_autotest=is_autotest,
            environment_id=environment_id,
            milestone_id=milestone_id,
            plan_id=plan_id,
            tags=tags,
            custom_field=custom_field,
            _configuration=_configuration,
            **kwargs,
        )
