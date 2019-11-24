from pydantic import PydanticValueError


class UsernameIsInvalidError(PydanticValueError):
    code = "username.invalid"
    msg_template = "str is not a valid username"
