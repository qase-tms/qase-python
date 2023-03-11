# qaseio.model.result_update.ResultUpdate

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**status** | str,  | str,  |  | [optional] must be one of ["in_progress", "passed", "failed", "blocked", "skipped", ] 
**time_ms** | None, decimal.Decimal, int,  | NoneClass, decimal.Decimal,  |  | [optional] value must be a 64 bit integer
**defect** | None, bool,  | NoneClass, BoolClass,  |  | [optional] 
**[attachments](#attachments)** | list, tuple, None,  | tuple, NoneClass,  |  | [optional] 
**stacktrace** | None, str,  | NoneClass, str,  |  | [optional] 
**comment** | None, str,  | NoneClass, str,  |  | [optional] 
**[steps](#steps)** | list, tuple, None,  | tuple, NoneClass,  |  | [optional] 
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

