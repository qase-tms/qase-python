# CustomFieldCreate


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**entity** | **int** | Possible values: 0 - case; 1 - run; 2 - defect;  | 
**type** | **int** | Possible values: 0 - number; 1 - string; 2 - text; 3 - selectbox; 4 - checkbox; 5 - radio; 6 - multiselect; 7 - url; 8 - user; 9 - datetime;  | 
**value** | [**[CustomFieldCreateValueInner], none_type**](CustomFieldCreateValueInner.md) | Required if type one of: 3 - selectbox; 5 - radio; 6 - multiselect;  | [optional] 
**placeholder** | **str, none_type** |  | [optional] 
**default_value** | **str, none_type** |  | [optional] 
**is_filterable** | **bool** |  | [optional] 
**is_visible** | **bool** |  | [optional] 
**is_required** | **bool** |  | [optional] 
**is_enabled_for_all_projects** | **bool** |  | [optional] 
**projects_codes** | **[str]** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


