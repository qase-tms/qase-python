from qaseio.api.custom_fields_api import CustomFieldsApi
from qaseio.utils.common import QaseClient, json_value, api_result


class CustomField(QaseClient):
    """Helper for CustomFieldsApi"""

    @api_result
    def get(self, field_id):
        """Get custom field result based on provided field id"""
        return CustomFieldsApi(self.client).get_custom_field(id=field_id)

    def get_title(self, field_id):
        """Get custom field name based on provided field id"""
        return self.get(field_id=field_id).title

    @json_value
    def get_value(self, field_id):
        """Get custom field result based on provided field id"""
        return self.get(field_id=field_id)
