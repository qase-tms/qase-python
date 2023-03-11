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


class SharedStepCreate(
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
            
            
                class MetaOapg:
                    max_length = 255
            action = schemas.StrSchema
            expected_result = schemas.StrSchema
            data = schemas.StrSchema
            
            
            class steps(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['SharedStepContentCreate']:
                        return SharedStepContentCreate
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['SharedStepContentCreate'], typing.List['SharedStepContentCreate']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'steps':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'SharedStepContentCreate':
                    return super().__getitem__(i)
            __annotations__ = {
                "title": title,
                "action": action,
                "expected_result": expected_result,
                "data": data,
                "steps": steps,
            }
    
    title: MetaOapg.properties.title
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["title"]) -> MetaOapg.properties.title: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["action"]) -> MetaOapg.properties.action: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["expected_result"]) -> MetaOapg.properties.expected_result: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["data"]) -> MetaOapg.properties.data: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["steps"]) -> MetaOapg.properties.steps: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["title", "action", "expected_result", "data", "steps", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["title"]) -> MetaOapg.properties.title: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["action"]) -> typing.Union[MetaOapg.properties.action, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["expected_result"]) -> typing.Union[MetaOapg.properties.expected_result, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["data"]) -> typing.Union[MetaOapg.properties.data, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["steps"]) -> typing.Union[MetaOapg.properties.steps, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["title", "action", "expected_result", "data", "steps", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        title: typing.Union[MetaOapg.properties.title, str, ],
        action: typing.Union[MetaOapg.properties.action, str, schemas.Unset] = schemas.unset,
        expected_result: typing.Union[MetaOapg.properties.expected_result, str, schemas.Unset] = schemas.unset,
        data: typing.Union[MetaOapg.properties.data, str, schemas.Unset] = schemas.unset,
        steps: typing.Union[MetaOapg.properties.steps, list, tuple, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'SharedStepCreate':
        return super().__new__(
            cls,
            *_args,
            title=title,
            action=action,
            expected_result=expected_result,
            data=data,
            steps=steps,
            _configuration=_configuration,
            **kwargs,
        )

from qaseio.model.shared_step_content_create import SharedStepContentCreate
