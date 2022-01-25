from pydantic.errors import PydanticErrorMixin


class AuthError(PydanticErrorMixin, Exception):
    base_name = "auth_error"


class InvalidCredentialsError(AuthError):
    code = "invalid_credentials"
    msg_template = "invalid credentials"


class NotAuthenticatedError(AuthError):
    code = "not_authenticated"
    msg_template = "authorization is required"


class NotAdminError(AuthError):
    code = "not_admin"
    msg_template = "administrator permission is required"


class NotModeratorError(AuthError):
    code = "not_moderator"
    msg_template = "moderator permission is required"
