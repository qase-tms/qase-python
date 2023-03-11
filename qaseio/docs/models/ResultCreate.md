# qaseio.model.result_create.ResultCreate

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**status** | str,  | str,  |  | must be one of ["in_progress", "passed", "failed", "blocked", "skipped", "invalid", ] 
**case_id** | decimal.Decimal, int,  | decimal.Decimal,  |  | [optional] value must be a 64 bit integer
**[case](#case)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Could be used instead of &#x60;case_id&#x60;. | [optional] 
**time** | None, decimal.Decimal, int,  | NoneClass, decimal.Decimal,  |  | [optional] value must be a 64 bit integer
**time_ms** | None, decimal.Decimal, int,  | NoneClass, decimal.Decimal,  |  | [optional] value must be a 64 bit integer
**defect** | None, bool,  | NoneClass, BoolClass,  |  | [optional] 
**[attachments](#attachments)** | list, tuple, None,  | tuple, NoneClass,  |  | [optional] 
**stacktrace** | None, str,  | NoneClass, str,  |  | [optional] 
**comment** | None, str,  | NoneClass, str,  |  | [optional] 
**[param](#param)** | dict, frozendict.frozendict, None,  | frozendict.frozendict, NoneClass,  | A map of parameters (name &#x3D;&gt; value) | [optional] 
**[steps](#steps)** | list, tuple, None,  | tuple, NoneClass,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# case

Could be used instead of `case_id`.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Could be used instead of &#x60;case_id&#x60;. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**title** | str,  | str,  |  | [optional] 
**suite_title** | None, str,  | NoneClass, str,  | Nested suites should be separated with &#x60;TAB&#x60; symbol. | [optional] 
**description** | None, str,  | NoneClass, str,  |  | [optional] 
**layer** | str,  | str,  |  | [optional] 
**severity** | str,  | str,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# attachments

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple, None,  | tuple, NoneClass,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# param

A map of parameters (name => value)

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, None,  | frozendict.frozendict, NoneClass,  | A map of parameters (name &#x3D;&gt; value) | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | str,  | str,  | any string name can be used but the value must be the correct type | [optional] 

# steps

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple, None,  | tuple, NoneClass,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**TestStepResultCreate**](TestStepResultCreate.md) | [**TestStepResultCreate**](TestStepResultCreate.md) | [**TestStepResultCreate**](TestStepResultCreate.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

