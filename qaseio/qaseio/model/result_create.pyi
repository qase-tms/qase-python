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


class ResultCreate(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "status",
        }
        
        class properties:
            
            
            class status(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def IN_PROGRESS(cls):
                    return cls("in_progress")
                
                @schemas.classproperty
                def PASSED(cls):
                    return cls("passed")
                
                @schemas.classproperty
                def FAILED(cls):
                    return cls("failed")
                
                @schemas.classproperty
                def BLOCKED(cls):
                    return cls("blocked")
                
                @schemas.classproperty
                def SKIPPED(cls):
                    return cls("skipped")
                
                @schemas.classproperty
                def INVALID(cls):
                    return cls("invalid")
            case_id = schemas.Int64Schema
            
            
            class case(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    
                    class properties:
                        title = schemas.StrSchema
                        
                        
                        class suite_title(
                            schemas.StrBase,
                            schemas.NoneBase,
                            schemas.Schema,
                            schemas.NoneStrMixin
                        ):
                        
                        
                            def __new__(
                                cls,
                                *_args: typing.Union[None, str, ],
                                _configuration: typing.Optional[schemas.Configuration] = None,
                            ) -> 'suite_title':
                                return super().__new__(
                                    cls,
                                    *_args,
                                    _configuration=_configuration,
                                )
                        
                        
                        class description(
                            schemas.StrBase,
                            schemas.NoneBase,
                            schemas.Schema,
                            schemas.NoneStrMixin
                        ):
                        
                        
                            def __new__(
                                cls,
                                *_args: typing.Union[None, str, ],
                                _configuration: typing.Optional[schemas.Configuration] = None,
                            ) -> 'description':
                                return super().__new__(
                                    cls,
                                    *_args,
                                    _configuration=_configuration,
                                )
                        layer = schemas.StrSchema
                        severity = schemas.StrSchema
                        __annotations__ = {
                            "title": title,
                            "suite_title": suite_title,
                            "description": description,
                            "layer": layer,
                            "severity": severity,
                        }
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["title"]) -> MetaOapg.properties.title: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["suite_title"]) -> MetaOapg.properties.suite_title: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["layer"]) -> MetaOapg.properties.layer: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["severity"]) -> MetaOapg.properties.severity: ...
                
                @typing.overload
                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                
                def __getitem__(self, name: typing.Union[typing_extensions.Literal["title", "suite_title", "description", "layer", "severity", ], str]):
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["title"]) -> typing.Union[MetaOapg.properties.title, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["suite_title"]) -> typing.Union[MetaOapg.properties.suite_title, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["description"]) -> typing.Union[MetaOapg.properties.description, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["layer"]) -> typing.Union[MetaOapg.properties.layer, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["severity"]) -> typing.Union[MetaOapg.properties.severity, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                
                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["title", "suite_title", "description", "layer", "severity", ], str]):
                    return super().get_item_oapg(name)
                
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, ],
                    title: typing.Union[MetaOapg.properties.title, str, schemas.Unset] = schemas.unset,
                    suite_title: typing.Union[MetaOapg.properties.suite_title, None, str, schemas.Unset] = schemas.unset,
                    description: typing.Union[MetaOapg.properties.description, None, str, schemas.Unset] = schemas.unset,
                    layer: typing.Union[MetaOapg.properties.layer, str, schemas.Unset] = schemas.unset,
                    severity: typing.Union[MetaOapg.properties.severity, str, schemas.Unset] = schemas.unset,
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'case':
                    return super().__new__(
                        cls,
                        *_args,
                        title=title,
                        suite_title=suite_title,
                        description=description,
                        layer=layer,
                        severity=severity,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class time(
                schemas.Int64Base,
                schemas.IntBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                class MetaOapg:
                    format = 'int64'
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, decimal.Decimal, int, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'time':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class time_ms(
                schemas.Int64Base,
                schemas.IntBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                class MetaOapg:
                    format = 'int64'
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, decimal.Decimal, int, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'time_ms':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class defect(
                schemas.BoolBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneBoolMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, bool, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'defect':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class attachments(
                schemas.ListBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneTupleMixin
            ):
            
            
                class MetaOapg:
                    items = schemas.StrSchema
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[list, tuple, None, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'attachments':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class stacktrace(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'stacktrace':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class comment(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'comment':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class param(
                schemas.DictBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneFrozenDictMixin
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
                    *_args: typing.Union[dict, frozendict.frozendict, None, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[MetaOapg.additional_properties, str, ],
                ) -> 'param':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class steps(
                schemas.ListBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneTupleMixin
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['TestStepResultCreate']:
                        return TestStepResultCreate
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[list, tuple, None, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'steps':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            __annotations__ = {
                "status": status,
                "case_id": case_id,
                "case": case,
                "time": time,
                "time_ms": time_ms,
                "defect": defect,
                "attachments": attachments,
                "stacktrace": stacktrace,
                "comment": comment,
                "param": param,
                "steps": steps,
            }
    
    status: MetaOapg.properties.status
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["case_id"]) -> MetaOapg.properties.case_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["case"]) -> MetaOapg.properties.case: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["time"]) -> MetaOapg.properties.time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["time_ms"]) -> MetaOapg.properties.time_ms: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["defect"]) -> MetaOapg.properties.defect: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["attachments"]) -> MetaOapg.properties.attachments: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["stacktrace"]) -> MetaOapg.properties.stacktrace: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["comment"]) -> MetaOapg.properties.comment: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["param"]) -> MetaOapg.properties.param: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["steps"]) -> MetaOapg.properties.steps: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["status", "case_id", "case", "time", "time_ms", "defect", "attachments", "stacktrace", "comment", "param", "steps", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["case_id"]) -> typing.Union[MetaOapg.properties.case_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["case"]) -> typing.Union[MetaOapg.properties.case, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["time"]) -> typing.Union[MetaOapg.properties.time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["time_ms"]) -> typing.Union[MetaOapg.properties.time_ms, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["defect"]) -> typing.Union[MetaOapg.properties.defect, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["attachments"]) -> typing.Union[MetaOapg.properties.attachments, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["stacktrace"]) -> typing.Union[MetaOapg.properties.stacktrace, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["comment"]) -> typing.Union[MetaOapg.properties.comment, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["param"]) -> typing.Union[MetaOapg.properties.param, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["steps"]) -> typing.Union[MetaOapg.properties.steps, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["status", "case_id", "case", "time", "time_ms", "defect", "attachments", "stacktrace", "comment", "param", "steps", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        status: typing.Union[MetaOapg.properties.status, str, ],
        case_id: typing.Union[MetaOapg.properties.case_id, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        case: typing.Union[MetaOapg.properties.case, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        time: typing.Union[MetaOapg.properties.time, None, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        time_ms: typing.Union[MetaOapg.properties.time_ms, None, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        defect: typing.Union[MetaOapg.properties.defect, None, bool, schemas.Unset] = schemas.unset,
        attachments: typing.Union[MetaOapg.properties.attachments, list, tuple, None, schemas.Unset] = schemas.unset,
        stacktrace: typing.Union[MetaOapg.properties.stacktrace, None, str, schemas.Unset] = schemas.unset,
        comment: typing.Union[MetaOapg.properties.comment, None, str, schemas.Unset] = schemas.unset,
        param: typing.Union[MetaOapg.properties.param, dict, frozendict.frozendict, None, schemas.Unset] = schemas.unset,
        steps: typing.Union[MetaOapg.properties.steps, list, tuple, None, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ResultCreate':
        return super().__new__(
            cls,
            *_args,
            status=status,
            case_id=case_id,
            case=case,
            time=time,
            time_ms=time_ms,
            defect=defect,
            attachments=attachments,
            stacktrace=stacktrace,
            comment=comment,
            param=param,
            steps=steps,
            _configuration=_configuration,
            **kwargs,
        )

from qaseio.model.test_step_result_create import TestStepResultCreate