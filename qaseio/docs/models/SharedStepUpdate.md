# qaseio.model.shared_step_update.SharedStepUpdate

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**title** | str,  | str,  |  | 
**action** | str,  | str,  | Deprecated, use the &#x60;steps&#x60; property instead. | [optional] 
**expected_result** | str,  | str,  | Deprecated, use the &#x60;steps&#x60; property instead. | [optional] 
**data** | str,  | str,  | Deprecated, use the &#x60;steps&#x60; property instead. | [optional] 
**[steps](#steps)** | list, tuple,  | tuple,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# steps

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**SharedStepContentCreate**](SharedStepContentCreate.md) | [**SharedStepContentCreate**](SharedStepContentCreate.md) | [**SharedStepContentCreate**](SharedStepContentCreate.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

