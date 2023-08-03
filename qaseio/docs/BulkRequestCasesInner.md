# BulkRequestCasesInner


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**description** | **str** |  | [optional] 
**preconditions** | **str** |  | [optional] 
**postconditions** | **str** |  | [optional] 
**severity** | **int** |  | [optional] 
**priority** | **int** |  | [optional] 
**behavior** | **int** |  | [optional] 
**type** | **int** |  | [optional] 
**layer** | **int** |  | [optional] 
**is_flaky** | **int** |  | [optional] 
**suite_id** | **int** |  | [optional] 
**milestone_id** | **int** |  | [optional] 
**automation** | **int** |  | [optional] 
**status** | **int** |  | [optional] 
**attachments** | [**AttachmentHashList**](AttachmentHashList.md) |  | [optional] 
**steps** | [**[TestStepCreate]**](TestStepCreate.md) |  | [optional] 
**tags** | **[str]** |  | [optional] 
**params** | **{str: ([str],)}, none_type** |  | [optional] 
**custom_field** | **{str: (str,)}** | A map of custom fields values (id &#x3D;&gt; value) | [optional] 
**created_at** | **str** |  | [optional] 
**updated_at** | **str** |  | [optional] 
**id** | **int, none_type** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


