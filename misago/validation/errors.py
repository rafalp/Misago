from pydantic import PydanticValueError

from ..types import AuthError


class AllFieldsAreRequiredError(PydanticValueError):
    code = "all_fields_are_required"
    msg_template = "all fields are required"


class NotAuthorizedError(AuthError):
    code = "not_authorized"
    msg_template = "authorization is required"


class EmailIsNotAvailableError(PydanticValueError):
    code = "email.not_available"
    msg_template = "e-mail is not available"


class InvalidCredentialsError(PydanticValueError):
    code = "invalid_credentials"
    msg_template = "invalid credentials"


class UsernameError(PydanticValueError):
    code = "username"
    msg_template = 'username does not match regex "{pattern}"'

    def __init__(  # pylint: disable=useless-super-delegation
        self, *, pattern: str
    ) -> None:
        super().__init__(pattern=pattern)


class UsernameIsNotAvailableError(PydanticValueError):
    code = "username.not_available"
    msg_template = "username is not available"
