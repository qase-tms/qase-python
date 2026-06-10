# TestCaseCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** |  | [optional] 
**preconditions** | **str** |  | [optional] 
**postconditions** | **str** |  | [optional] 
**title** | **str** |  | 
**severity** | **int** |  | [optional] 
**priority** | **int** |  | [optional] 
**behavior** | **int** |  | [optional] 
**type** | **int** |  | [optional] 
**layer** | **int** |  | [optional] 
**is_flaky** | **int** |  | [optional] 
**suite_id** | **int** |  | [optional] 
**milestone_id** | **int** |  | [optional] 
**automation** | **int** | Deprecated, use &#x60;isManual&#x60; and &#x60;isToBeAutomated&#x60; instead. Encodes the test case automation state as a single integer: &#x60;0&#x60; &#x3D; manual, &#x60;1&#x60; &#x3D; manual planned to be automated, &#x60;2&#x60; &#x3D; automated. If both &#x60;automation&#x60; and &#x60;isManual&#x60;/&#x60;isToBeAutomated&#x60; are provided, &#x60;isManual&#x60; and &#x60;isToBeAutomated&#x60; take precedence. | [optional] 
**is_manual** | **int** | &#x60;1&#x60; if the case is manual, &#x60;0&#x60; if it is automated. Combined with &#x60;isToBeAutomated&#x60;, replaces the deprecated &#x60;automation&#x60; field. | [optional] 
**is_to_be_automated** | **int** | &#x60;1&#x60; if a manual case is planned to be automated, &#x60;0&#x60; otherwise. Only meaningful when &#x60;isManual &#x3D; 1&#x60;; ignored when &#x60;isManual &#x3D; 0&#x60;. | [optional] 
**status** | **int** |  | [optional] 
**steps_type** | **str** | Determines the format of the steps field. When \&quot;classic\&quot;, steps use the standard action/expected_result/data format. When \&quot;gherkin\&quot;, steps use the {value: \&quot;Given...\\nWhen...\\nThen...\&quot;} format. | [optional] [default to 'classic']
**attachments** | **List[str]** | A list of Attachment hashes. | [optional] 
**steps** | [**List[TestStepCreate]**](TestStepCreate.md) |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**params** | **Dict[str, List[str]]** | Deprecated, use &#x60;parameters&#x60; instead. | [optional] 
**parameters** | [**List[TestCaseParameterCreate]**](TestCaseParameterCreate.md) |  | [optional] 
**custom_field** | **Dict[str, str]** | Custom field values keyed by the field&#39;s project-scoped &#x60;internal_id&#x60; (see &#x60;GET /custom_field&#x60;). Values are always **scalar strings**; arrays, objects or non-scalars are rejected.  | Field type           | Value format                              | Example                 | |----------------------|-------------------------------------------|-------------------------| | &#x60;string&#x60;, &#x60;text&#x60;     | Plain string                              | &#x60;\&quot;hello\&quot;&#x60;               | | &#x60;number&#x60;             | Numeric string                            | &#x60;\&quot;42\&quot;&#x60;                  | | &#x60;url&#x60;                | Valid URL                                 | &#x60;\&quot;https://qase.io\&quot;&#x60;     | | &#x60;datetime&#x60;           | Absolute date (ISO 8601 recommended)      | &#x60;\&quot;2026-04-29T15:00:00Z\&quot;&#x60;| | &#x60;selectbox&#x60;, &#x60;radio&#x60; | Option &#x60;id&#x60; as string                     | &#x60;\&quot;1\&quot;&#x60;                   | | &#x60;multiselect&#x60;        | Comma-separated option &#x60;id&#x60;s (no spaces)  | &#x60;\&quot;1,2,3\&quot;&#x60;               | | &#x60;checkbox&#x60;           | &#x60;\&quot;1\&quot;&#x60; to check, &#x60;\&quot;\&quot;&#x60; to uncheck           | &#x60;\&quot;1\&quot;&#x60;                   | | &#x60;user&#x60;               | Team member &#x60;internal_id&#x60; as string       | &#x60;\&quot;42\&quot;&#x60;                  |  Validation: all required fields without a default value must be present and non-empty; unknown &#x60;internal_id&#x60;s are rejected; option-based values must reference an existing option.  Note: a &#x60;required&#x60; checkbox without a default cannot be unchecked via the API — set a default or clear &#x60;required&#x60; in workspace settings.  | [optional] 
**created_at** | **str** |  | [optional] 
**updated_at** | **str** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.test_case_create import TestCaseCreate

# TODO update the JSON string below
json = "{}"
# create an instance of TestCaseCreate from a JSON string
test_case_create_instance = TestCaseCreate.from_json(json)
# print the JSON string representation of the object
print(TestCaseCreate.to_json())

# convert the object into a dict
test_case_create_dict = test_case_create_instance.to_dict()
# create an instance of TestCaseCreate from a dict
test_case_create_from_dict = TestCaseCreate.from_dict(test_case_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


