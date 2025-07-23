# RunCreateCloudRunConfig

Configuration for the cloud run, if applicable

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**browser** | **str** | The browser to be used for the cloud run | [optional] 

## Example

```python
from qase.api_client_v1.models.run_create_cloud_run_config import RunCreateCloudRunConfig

# TODO update the JSON string below
json = "{}"
# create an instance of RunCreateCloudRunConfig from a JSON string
run_create_cloud_run_config_instance = RunCreateCloudRunConfig.from_json(json)
# print the JSON string representation of the object
print(RunCreateCloudRunConfig.to_json())

# convert the object into a dict
run_create_cloud_run_config_dict = run_create_cloud_run_config_instance.to_dict()
# create an instance of RunCreateCloudRunConfig from a dict
run_create_cloud_run_config_form_dict = run_create_cloud_run_config.from_dict(run_create_cloud_run_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


