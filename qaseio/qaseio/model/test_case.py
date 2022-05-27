"""
    Qase.io API

    Qase API Specification.  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: support@qase.io
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from qaseio.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
    OpenApiModel
)
from qaseio.exceptions import ApiAttributeError


def lazy_import():
    from qaseio.model.attachment import Attachment
    from qaseio.model.custom_field_value import CustomFieldValue
    from qaseio.model.tag_value import TagValue
    from qaseio.model.test_step import TestStep
    globals()['Attachment'] = Attachment
    globals()['CustomFieldValue'] = CustomFieldValue
    globals()['TagValue'] = TagValue
    globals()['TestStep'] = TestStep


class TestCase(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
    }

    validations = {
    }

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        lazy_import()
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        lazy_import()
        return {
            'id': (int,),  # noqa: E501
            'position': (int,),  # noqa: E501
            'title': (str,),  # noqa: E501
            'description': (str, none_type,),  # noqa: E501
            'preconditions': (str, none_type,),  # noqa: E501
            'postconditions': (str, none_type,),  # noqa: E501
            'severity': (int,),  # noqa: E501
            'priority': (int,),  # noqa: E501
            'type': (int,),  # noqa: E501
            'layer': (int,),  # noqa: E501
            'is_flaky': (int,),  # noqa: E501
            'behavior': (int,),  # noqa: E501
            'automation': (int,),  # noqa: E501
            'status': (int,),  # noqa: E501
            'milestone_id': (int, none_type,),  # noqa: E501
            'suite_id': (int, none_type,),  # noqa: E501
            'custom_fields': ([CustomFieldValue],),  # noqa: E501
            'attachments': ([Attachment],),  # noqa: E501
            'steps_type': (str, none_type,),  # noqa: E501
            'steps': ([TestStep],),  # noqa: E501
            'params': (bool, date, datetime, dict, float, int, list, str, none_type,),  # noqa: E501
            'tags': ([TagValue],),  # noqa: E501
            'member_id': (int,),  # noqa: E501
            'project_id': (int,),  # noqa: E501
            'created_at': (datetime,),  # noqa: E501
            'updated_at': (datetime,),  # noqa: E501
            'deleted': (str, none_type,),  # noqa: E501
            'created': (str,),  # noqa: E501
            'updated': (str,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'id': 'id',  # noqa: E501
        'position': 'position',  # noqa: E501
        'title': 'title',  # noqa: E501
        'description': 'description',  # noqa: E501
        'preconditions': 'preconditions',  # noqa: E501
        'postconditions': 'postconditions',  # noqa: E501
        'severity': 'severity',  # noqa: E501
        'priority': 'priority',  # noqa: E501
        'type': 'type',  # noqa: E501
        'layer': 'layer',  # noqa: E501
        'is_flaky': 'is_flaky',  # noqa: E501
        'behavior': 'behavior',  # noqa: E501
        'automation': 'automation',  # noqa: E501
        'status': 'status',  # noqa: E501
        'milestone_id': 'milestone_id',  # noqa: E501
        'suite_id': 'suite_id',  # noqa: E501
        'custom_fields': 'custom_fields',  # noqa: E501
        'attachments': 'attachments',  # noqa: E501
        'steps_type': 'steps_type',  # noqa: E501
        'steps': 'steps',  # noqa: E501
        'params': 'params',  # noqa: E501
        'tags': 'tags',  # noqa: E501
        'member_id': 'member_id',  # noqa: E501
        'project_id': 'project_id',  # noqa: E501
        'created_at': 'created_at',  # noqa: E501
        'updated_at': 'updated_at',  # noqa: E501
        'deleted': 'deleted',  # noqa: E501
        'created': 'created',  # noqa: E501
        'updated': 'updated',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """TestCase - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            id (int): [optional]  # noqa: E501
            position (int): [optional]  # noqa: E501
            title (str): [optional]  # noqa: E501
            description (str, none_type): [optional]  # noqa: E501
            preconditions (str, none_type): [optional]  # noqa: E501
            postconditions (str, none_type): [optional]  # noqa: E501
            severity (int): [optional]  # noqa: E501
            priority (int): [optional]  # noqa: E501
            type (int): [optional]  # noqa: E501
            layer (int): [optional]  # noqa: E501
            is_flaky (int): [optional]  # noqa: E501
            behavior (int): [optional]  # noqa: E501
            automation (int): [optional]  # noqa: E501
            status (int): [optional]  # noqa: E501
            milestone_id (int, none_type): [optional]  # noqa: E501
            suite_id (int, none_type): [optional]  # noqa: E501
            custom_fields ([CustomFieldValue]): [optional]  # noqa: E501
            attachments ([Attachment]): [optional]  # noqa: E501
            steps_type (str, none_type): [optional]  # noqa: E501
            steps ([TestStep]): [optional]  # noqa: E501
            params (bool, date, datetime, dict, float, int, list, str, none_type): [optional]  # noqa: E501
            tags ([TagValue]): [optional]  # noqa: E501
            member_id (int): [optional]  # noqa: E501
            project_id (int): [optional]  # noqa: E501
            created_at (datetime): [optional]  # noqa: E501
            updated_at (datetime): [optional]  # noqa: E501
            deleted (str, none_type): [optional]  # noqa: E501
            created (str): Deprecated, use the `created_at` property instead.. [optional]  # noqa: E501
            updated (str): Deprecated, use the `updated_at` property instead.. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, *args, **kwargs):  # noqa: E501
        """TestCase - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            id (int): [optional]  # noqa: E501
            position (int): [optional]  # noqa: E501
            title (str): [optional]  # noqa: E501
            description (str, none_type): [optional]  # noqa: E501
            preconditions (str, none_type): [optional]  # noqa: E501
            postconditions (str, none_type): [optional]  # noqa: E501
            severity (int): [optional]  # noqa: E501
            priority (int): [optional]  # noqa: E501
            type (int): [optional]  # noqa: E501
            layer (int): [optional]  # noqa: E501
            is_flaky (int): [optional]  # noqa: E501
            behavior (int): [optional]  # noqa: E501
            automation (int): [optional]  # noqa: E501
            status (int): [optional]  # noqa: E501
            milestone_id (int, none_type): [optional]  # noqa: E501
            suite_id (int, none_type): [optional]  # noqa: E501
            custom_fields ([CustomFieldValue]): [optional]  # noqa: E501
            attachments ([Attachment]): [optional]  # noqa: E501
            steps_type (str, none_type): [optional]  # noqa: E501
            steps ([TestStep]): [optional]  # noqa: E501
            params (bool, date, datetime, dict, float, int, list, str, none_type): [optional]  # noqa: E501
            tags ([TagValue]): [optional]  # noqa: E501
            member_id (int): [optional]  # noqa: E501
            project_id (int): [optional]  # noqa: E501
            created_at (datetime): [optional]  # noqa: E501
            updated_at (datetime): [optional]  # noqa: E501
            deleted (str, none_type): [optional]  # noqa: E501
            created (str): Deprecated, use the `created_at` property instead.. [optional]  # noqa: E501
            updated (str): Deprecated, use the `updated_at` property instead.. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")
