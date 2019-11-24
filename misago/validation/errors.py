from pydantic import PydanticValueError


class EmailIsNotAvailableError(PydanticValueError):
    code = "email.not-available"
    msg_template = "this e-mail is not available"


class UsernameIsNotAvailableError(PydanticValueError):
    code = "username.not-available"
    msg_template = "this username is not available"
