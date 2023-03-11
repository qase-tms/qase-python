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


class SharedStep(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
            hash = schemas.StrSchema
            title = schemas.StrSchema
            action = schemas.StrSchema
            expected_result = schemas.StrSchema
            
            
            class steps(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['SharedStepContent']:
                        return SharedStepContent
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['SharedStepContent'], typing.List['SharedStepContent']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'steps':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'SharedStepContent':
                    return super().__getitem__(i)
            data = schemas.StrSchema
            
            
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
            cases_count = schemas.IntSchema
            created = schemas.StrSchema
            updated = schemas.StrSchema
            created_at = schemas.DateTimeSchema
            updated_at = schemas.DateTimeSchema
            __annotations__ = {
                "hash": hash,
                "title": title,
                "action": action,
                "expected_result": expected_result,
                "steps": steps,
                "data": data,
                "cases": cases,
                "cases_count": cases_count,
                "created": created,
                "updated": updated,
                "created_at": created_at,
                "updated_at": updated_at,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["hash"]) -> MetaOapg.properties.hash: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["title"]) -> MetaOapg.properties.title: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["action"]) -> MetaOapg.properties.action: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["expected_result"]) -> MetaOapg.properties.expected_result: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["steps"]) -> MetaOapg.properties.steps: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["data"]) -> MetaOapg.properties.data: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["cases"]) -> MetaOapg.properties.cases: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["cases_count"]) -> MetaOapg.properties.cases_count: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["created"]) -> MetaOapg.properties.created: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["updated"]) -> MetaOapg.properties.updated: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["created_at"]) -> MetaOapg.properties.created_at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["updated_at"]) -> MetaOapg.properties.updated_at: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["hash", "title", "action", "expected_result", "steps", "data", "cases", "cases_count", "created", "updated", "created_at", "updated_at", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["hash"]) -> typing.Union[MetaOapg.properties.hash, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["title"]) -> typing.Union[MetaOapg.properties.title, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["action"]) -> typing.Union[MetaOapg.properties.action, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["expected_result"]) -> typing.Union[MetaOapg.properties.expected_result, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["steps"]) -> typing.Union[MetaOapg.properties.steps, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["data"]) -> typing.Union[MetaOapg.properties.data, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["cases"]) -> typing.Union[MetaOapg.properties.cases, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["cases_count"]) -> typing.Union[MetaOapg.properties.cases_count, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["created"]) -> typing.Union[MetaOapg.properties.created, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["updated"]) -> typing.Union[MetaOapg.properties.updated, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["created_at"]) -> typing.Union[MetaOapg.properties.created_at, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["updated_at"]) -> typing.Union[MetaOapg.properties.updated_at, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["hash", "title", "action", "expected_result", "steps", "data", "cases", "cases_count", "created", "updated", "created_at", "updated_at", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        hash: typing.Union[MetaOapg.properties.hash, str, schemas.Unset] = schemas.unset,
        title: typing.Union[MetaOapg.properties.title, str, schemas.Unset] = schemas.unset,
        action: typing.Union[MetaOapg.properties.action, str, schemas.Unset] = schemas.unset,
        expected_result: typing.Union[MetaOapg.properties.expected_result, str, schemas.Unset] = schemas.unset,
        steps: typing.Union[MetaOapg.properties.steps, list, tuple, schemas.Unset] = schemas.unset,
        data: typing.Union[MetaOapg.properties.data, str, schemas.Unset] = schemas.unset,
        cases: typing.Union[MetaOapg.properties.cases, list, tuple, schemas.Unset] = schemas.unset,
        cases_count: typing.Union[MetaOapg.properties.cases_count, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        created: typing.Union[MetaOapg.properties.created, str, schemas.Unset] = schemas.unset,
        updated: typing.Union[MetaOapg.properties.updated, str, schemas.Unset] = schemas.unset,
        created_at: typing.Union[MetaOapg.properties.created_at, str, datetime, schemas.Unset] = schemas.unset,
        updated_at: typing.Union[MetaOapg.properties.updated_at, str, datetime, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'SharedStep':
        return super().__new__(
            cls,
            *_args,
            hash=hash,
            title=title,
            action=action,
            expected_result=expected_result,
            steps=steps,
            data=data,
            cases=cases,
            cases_count=cases_count,
            created=created,
            updated=updated,
            created_at=created_at,
            updated_at=updated_at,
            _configuration=_configuration,
            **kwargs,
        )

from qaseio.model.shared_step_content import SharedStepContent
