# QqlTestCase


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**position** | **int** |  | [optional] 
**title** | **str** |  | [optional] 
**description** | **str, none_type** |  | [optional] 
**preconditions** | **str, none_type** |  | [optional] 
**postconditions** | **str, none_type** |  | [optional] 
**severity** | **int** |  | [optional] 
**priority** | **int** |  | [optional] 
**type** | **int** |  | [optional] 
**layer** | **int** |  | [optional] 
**is_flaky** | **int** |  | [optional] 
**behavior** | **int** |  | [optional] 
**automation** | **int** |  | [optional] 
**status** | **int** |  | [optional] 
**milestone_id** | **int, none_type** |  | [optional] 
**suite_id** | **int, none_type** |  | [optional] 
**custom_fields** | [**[CustomFieldValue]**](CustomFieldValue.md) |  | [optional] 
**attachments** | [**[Attachment]**](Attachment.md) |  | [optional] 
**steps_type** | **str, none_type** |  | [optional] 
**steps** | [**[TestStep]**](TestStep.md) |  | [optional] 
**params** | [**TestCaseParams**](TestCaseParams.md) |  | [optional] 
**tags** | [**[TagValue]**](TagValue.md) |  | [optional] 
**member_id** | **int** | Deprecated, use &#x60;author_id&#x60; instead. | [optional] 
**author_id** | **int** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


