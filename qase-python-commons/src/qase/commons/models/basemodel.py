import json

from enum import Enum


class BaseModel:
    def __str__(self, enum_as_name=False) -> str:
        def serialize(o):
            if isinstance(o, Enum):
                return o.name if enum_as_name else o.value
            elif hasattr(o, '__dict__'):
                return o.__dict__
            else:
                return str(o)

        return json.dumps(self, default=serialize, indent=4, sort_keys=True)
