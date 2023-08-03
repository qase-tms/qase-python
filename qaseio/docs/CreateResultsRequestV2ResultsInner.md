# CreateResultsRequestV2ResultsInner


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**title** | **str** |  | [optional] 
**signature** | **str** |  | [optional] 
**testops_id** | **int, none_type** |  | [optional] 
**case_id** | **int, none_type** |  | [optional] 
**suite_id** | **int, none_type** |  | [optional] 
**execution** | [**ResultExecution**](ResultExecution.md) |  | [optional] 
**fields** | **{str: (str,)}** |  | [optional] 
**attachments** | [**[ResultAttachment]**](ResultAttachment.md) |  | [optional] 
**steps** | [**[ResultStep]**](ResultStep.md) |  | [optional] 
**params** | **{str: (str,)}** |  | [optional] 
**author** | **str** |  | [optional] 
**relations** | [**ResultRelations**](ResultRelations.md) |  | [optional] 
**muted** | **bool** |  | [optional] 
**message** | **str** |  | [optional] 
**created_at** | **float, none_type** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


