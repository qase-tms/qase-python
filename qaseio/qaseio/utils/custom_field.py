from qaseio.api.custom_fields_api import CustomFieldsApi
from qaseio.utils.common import QaseClient


class CustomField(QaseClient):
    """Helper for CustomFieldsApi"""

    def get(self, field_id):
        """Get custom field based on provided field id"""
        return self.get_value(CustomFieldsApi(self.client).get_custom_field(id=field_id))
