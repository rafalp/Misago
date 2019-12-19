from pydantic.errors import PydanticErrorMixin


class AuthError(PydanticErrorMixin, Exception):
    pass
