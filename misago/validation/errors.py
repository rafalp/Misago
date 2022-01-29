from pydantic.errors import PydanticErrorMixin, PydanticTypeError, PydanticValueError


class BaseError(PydanticErrorMixin, Exception):
    pass


VALIDATION_ERRORS = (BaseError, PydanticValueError, PydanticTypeError)
