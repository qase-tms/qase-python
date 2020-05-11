from enum import Enum, unique

import attr


@unique
class AccessLevel(Enum):
    ALL = "all"
    GROUP = "group"
    NONE = "none"


@unique
class Severity(Enum):
    UNDEFINED = "undefined"
    BLOCKER = "blocker"
    CRITICAL = "critical"
    MAJOR = "major"
    NORMAL = "normal"
    MINOR = "minor"
    TRIVIAL = "trivial"


@unique
class Priority(Enum):
    UNDEFINED = "undefined"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@unique
class Type(Enum):
    OTHER = "other"
    FUNCTIONAL = "functional"
    SMOKE = "smoke"
    REGRESSION = "regression"
    SECURITY = "security"
    USABILITY = "usability"
    PERFORMANCE = "performance"
    ACCEPTANCE = "acceptance"


@unique
class Behavior(Enum):
    UNDEFINED = "undefined"
    POSITIVE = "positive"
    NEGATIVE = "negative"
    DESTRUCTIVE = "destructive"


@unique
class Automation(Enum):
    IS_NOT_AUTOMATED = "is-not-automated"
    AUTOMATED = "automated"
    TO_BE_AUTOMATED = "to-be-automated"


@attr.s
class DefaultList:
    total: int = attr.ib(default=None)
    filtered: int = attr.ib(default=None)
    count: int = attr.ib(default=None)


@attr.s
class DefaultFilter:
    _is_filter = True

    def _no_enum(self, value):
        if isinstance(value, Enum):
            return value.value
        return value

    def filter(self):
        from apitist.utils import is_sequence

        fields = attr.fields(type(self))
        filters = {}
        for field in fields:
            name = field.name
            values = getattr(self, field.name)
            if (
                values is not None
                and is_sequence(field.type)
                and isinstance(values, list)
            ):
                values = ",".join([self._no_enum(val) for val in values])
            else:
                values = self._no_enum(values)
            if values:
                filters[f"filters[{name}]"] = values
        return filters
