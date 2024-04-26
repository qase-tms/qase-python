import json


class BaseModel:
    def __str__(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__ if hasattr(o, '__dict__') else str(o), indent=4,
                          sort_keys=True)
