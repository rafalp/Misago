from pydantic import PydanticValueError


class EmailIsNotAvailableError(PydanticValueError):
    code = "email.not_available"
    msg_template = "e-mail is not available"


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
