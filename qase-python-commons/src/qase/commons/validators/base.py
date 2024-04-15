class BaseValidator:
    def __init__(self, value):
        self.value = value

    def validate(self):
        raise NotImplementedError("Method validate not implemented")
