# qaseio.model.shared_step.SharedStep

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**hash** | str,  | str,  |  | [optional] 
**title** | str,  | str,  |  | [optional] 
**action** | str,  | str,  |  | [optional] 
**expected_result** | str,  | str,  |  | [optional] 
**[steps](#steps)** | list, tuple,  | tuple,  |  | [optional] 
**data** | str,  | str,  |  | [optional] 
**[cases](#cases)** | list, tuple,  | tuple,  |  | [optional] 
**cases_count** | decimal.Decimal, int,  | decimal.Decimal,  |  | [optional] 
**created** | str,  | str,  | Deprecated, use the &#x60;created_at&#x60; property instead. | [optional] 
**updated** | str,  | str,  | Deprecated, use the &#x60;updated_at&#x60; property instead. | [optional] 
**created_at** | str, datetime,  | str,  |  | [optional] value must conform to RFC-3339 date-time
**updated_at** | str, datetime,  | str,  |  | [optional] value must conform to RFC-3339 date-time
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# steps

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**SharedStepContent**](SharedStepContent.md) | [**SharedStepContent**](SharedStepContent.md) | [**SharedStepContent**](SharedStepContent.md) |  | 

# cases

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | decimal.Decimal, int,  | decimal.Decimal,  |  | value must be a 64 bit integer

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

