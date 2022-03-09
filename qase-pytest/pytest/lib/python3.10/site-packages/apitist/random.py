import inspect
import random as rnd
import typing
from dataclasses import MISSING, fields, is_dataclass

import attr

from apitist.utils import (
    has_args,
    is_attrs_class,
    is_sequence,
    is_tuple,
    is_union_type,
)

from .logging import Logging

T = typing.TypeVar("T")


def str_type(name: str):
    return type(name, (str,), {})


Address = str_type("Address")
Country = str_type("Country")
CountryCode = str_type("CountryCode")
PostCode = str_type("PostCode")
StreetAddress = str_type("StreetAddress")
CarNumber = str_type("CarNumber")
BBAN = str_type("BBAN")
IBAN = str_type("IBAN")
SWIFT11 = str_type("SWIFT11")
SWIFT8 = str_type("SWIFT8")
CreditCardExpire = str_type("CreditCardExpire")
CreditCardNumber = str_type("CreditCardNumber")
CreditCardProvider = str_type("CreditCardProvider")
CreditCardSecurityCode = str_type("CreditCardSecurityCode")
CompanyName = str_type("CompanyName")
CompanySuffix = str_type("CompanySuffix")
FileName = str_type("FileName")
Ipv4 = str_type("Ipv4")
Ipv6 = str_type("Ipv6")
MacAddress = str_type("MacAddress")
UserAgent = str_type("UserAgent")
URI = str_type("URI")
Email = str_type("Email")
Username = str_type("Username")
FirstName = str_type("FirstName")
LastName = str_type("LastName")
Patronymic = str_type("Patronymic")
PhoneNumber = str_type("PhoneNumber")
Job = str_type("Job")
Paragraph = str_type("Paragraph")
Date = str_type("Date")


class Randomer:
    _types_dict = None

    def __init__(self):
        self._types_dict = dict()

    @property
    def available_hooks(self):
        return self._types_dict

    def get_hook(self, t: typing.Type):
        """Get function for given type"""
        func = self._types_dict.get(t)
        if func is None:
            raise TypeError("Unable to find hook for {} type".format(t))
        return func

    def run_hook(self, t: typing.Type, **set_params):
        """Generate random data for given type"""
        func = self.get_hook(t)
        if inspect.getfullargspec(func).varkw:
            Logging.logger.debug(
                "All additional params will be passed to hook: %s", set_params
            )
            res = func(**set_params)
        else:
            res = func()
        Logging.logger.debug("Generated data for type %s: %s", t, res)
        return res

    def add_type(self, t: typing.Type[T], func: typing.Callable[[], T]):
        """
        Add new type for random generation.
        Function should return given type.
        """
        if t in self._types_dict:
            Logging.logger.warning(
                "Type %s already exists in dict, overriding", t
            )
        Logging.logger.debug("Registering type %s with function %s", t, func)
        self._types_dict[t] = func

    def add_types(
        self, types_dict: typing.Dict[typing.Type[T], typing.Callable[[], T]]
    ):
        """
        Add new types for random generation.
        Functions should return given type.
        """
        Logging.logger.debug("Registering list of types: %s", types_dict)
        self._types_dict.update(types_dict)

    def add_predefined(self, **kwargs):
        try:
            import faker
        except ModuleNotFoundError:
            raise ImportError(
                "Please pre-install Faker:"
                "\n\tpip install -e 'apitist[random]'"
                "\n\tor"
                "\n\tpip install faker"
            )
        fake = faker.Faker(**kwargs)
        types = {
            str: fake.pystr,
            int: fake.pyint,
            float: fake.pyfloat,
            bool: fake.pybool,
            list: fake.pylist,
            Address: fake.address,
            Country: fake.country,
            CountryCode: fake.country_code,
            PostCode: fake.postcode,
            StreetAddress: fake.street_address,
            CarNumber: fake.license_plate,
            BBAN: fake.bban,
            IBAN: fake.iban,
            SWIFT11: fake.swift11,
            SWIFT8: fake.swift8,
            CreditCardExpire: fake.credit_card_expire,
            CreditCardNumber: fake.credit_card_number,
            CreditCardProvider: fake.credit_card_provider,
            CreditCardSecurityCode: fake.credit_card_security_code,
            CompanyName: fake.company,
            CompanySuffix: fake.company_suffix,
            FileName: fake.file_name,
            Ipv4: fake.ipv4,
            Ipv6: fake.ipv6,
            MacAddress: fake.mac_address,
            UserAgent: fake.user_agent,
            URI: fake.uri,
            Email: lambda: fake.email(),
            Username: lambda: fake.user_name(),
            FirstName: fake.first_name,
            LastName: fake.last_name,
            Patronymic: fake.first_name_male,
            PhoneNumber: fake.phone_number,
            Job: fake.job,
            Paragraph: fake.paragraph,
            Date: fake.date,
        }
        self.add_types(types)

    def random_object(
        self,
        t: typing.Type[T],
        required_only=False,
        ignore: typing.List[str] = None,
        only: typing.List[str] = None,
        inverse=False,
        **set_params,
    ) -> T:
        """
        Create object of given type with random data

        Be careful, random object does not use converter to create a type
        It may lead to types missmatch

        :param t: Type which would me generated randomly
        :param required_only: Use only fields which do not have default values
        :param ignore: List of fields which should be ignored
            (will be passed to hook kwargs)
        :param only: List of fields which should be used
            (just a workaround near ignore + inverse)
        :param inverse: Inverse ignore list (will be passed to hook kwargs)
        :param set_params: Custom params which would be manually set to type
            (will be passed to hook kwargs)
        :return: Object of given type
        """
        Logging.logger.debug("Generating random data for type %s", t)
        if only and ignore:
            raise ValueError(
                "Only one of parameters - only or ignore should be used"
            )
        if only:
            ignore = only
            inverse = True
        if ignore is None:
            ignore = list()
        if t in self.available_hooks:
            return self.run_hook(
                t, ignore=ignore, inverse=inverse, **set_params
            )
        elif is_attrs_class(t):
            data = {}
            for field in attr.fields(t):
                f_name = field.name
                has_default = field.default is not attr.NOTHING
                if f_name in set_params:
                    data[f_name] = set_params[f_name]
                    continue
                if (
                    (f_name in ignore and inverse is False)
                    or (ignore and f_name not in ignore and inverse is True)
                    or (required_only and has_default)
                ):
                    data[f_name] = field.default if has_default else None
                    continue
                data[f_name] = self.random_object(
                    field.type,
                    required_only=required_only,
                    ignore=ignore,
                    inverse=inverse,
                    **set_params,
                )
            data = t(**data)
            Logging.logger.debug(
                "Generating random data for attrs type %s", data
            )
            return data
        elif is_dataclass(t):
            data = {}
            for field in fields(t):
                f_name = field.name
                has_default = (
                    field.default is not MISSING
                    or field.default_factory is not MISSING
                )
                if f_name in set_params:
                    data[f_name] = set_params[f_name]
                    continue
                if (
                    (f_name in ignore and inverse is False)
                    or (ignore and f_name not in ignore and inverse is True)
                    or (required_only and has_default)
                ):
                    data[f_name] = None
                    if has_default:
                        data[f_name] = (
                            field.default
                            if field.default != MISSING
                            else field.default_factory()
                        )
                    continue
                data[f_name] = self.random_object(
                    field.type,
                    required_only=required_only,
                    ignore=ignore,
                    inverse=inverse,
                    **set_params,
                )
            data = t(**data)
            Logging.logger.debug(
                "Generating random data for dataclass type %s", data
            )
            return data
        elif is_union_type(t) and has_args(t):
            return self.random_object(
                rnd.choice(t.__args__),
                required_only=required_only,
                ignore=ignore,
                inverse=inverse,
                **set_params,
            )
        elif is_tuple(t) and has_args(t):
            return (
                self.random_object(
                    t.__args__[0],
                    required_only=required_only,
                    ignore=ignore,
                    inverse=inverse,
                    **set_params,
                ),
            )
        elif is_sequence(t) and has_args(t):
            return [
                self.random_object(
                    t.__args__[0],
                    required_only=required_only,
                    ignore=ignore,
                    inverse=inverse,
                    **set_params,
                )
            ]
        return None

    object = random_object

    def random_partial(
        self, t: typing.Type[T], use: list = (), **set_params
    ) -> T:
        """
        Create object of given type with random data with only given fields.
        """
        if t in self.available_hooks:
            return self.run_hook(t, use=use, **set_params)
        elif is_attrs_class(t):
            data = {}
            for field in attr.fields(t):
                key = field.name
                if set_params and key in set_params:
                    data[key] = set_params[key]
                    continue
                if (
                    use
                    and key not in use
                    and (
                        not is_attrs_class(field.type)
                        or (
                            is_attrs_class(field.type)
                            and field.type in self.available_hooks
                        )
                    )
                ):
                    data[key] = attr.NOTHING
                    continue
                data[key] = self.random_partial(field.type, use, **set_params)

            if not all(v == attr.NOTHING for _, v in data.items()):
                return t(**data)
            return attr.NOTHING

        elif is_dataclass(t):
            data = {}
            for field in fields(t):
                key = field.name
                if set_params and key in set_params:
                    data[key] = set_params[key]
                    continue
                if (
                    use
                    and key not in use
                    and (
                        not is_dataclass(field.type)
                        or (
                            is_dataclass(field.type)
                            and field.type in self.available_hooks
                        )
                    )
                ):
                    data[key] = MISSING
                    continue

                data[key] = self.random_partial(field.type, use, **set_params)

            if not all(v == MISSING for _, v in data.items()):
                return t(**data)
            return MISSING

        elif is_union_type(t) and has_args(t):
            return self.random_partial(
                rnd.choice(t.__args__), use=use, **set_params
            )
        elif is_tuple(t) and has_args(t):
            return (self.random_partial(t.__args__[0], use=use, **set_params),)
        elif is_sequence(t) and has_args(t):
            return [self.random_partial(t.__args__[0], use=use, **set_params)]
        return None

    partial = random_partial
