from typing import Any, Sequence

from bh.core_utils.bh_exception import BHException


class MissingParameters(BHException):
    STATUS_CODE = 400

    @classmethod
    def from_args(cls, params_list: Sequence[str]) -> Any:
        return cls(f"Missing parameters in the request. Please specify all these parameters: {params_list}")


class MissingOptionalParameters(MissingParameters):
    @classmethod
    def from_args(cls, params_list: Sequence[str]) -> Any:
        return cls(f"Missing optional parameters in the request. Please specify one of these parameters: {params_list}")


class InvalidTokens(BHException):
    STATUS_CODE = 401


class ExpiredRefreshToken(BHException):
    STATUS_CODE = 401  # forces client to login again


class UserAccountAuthExceptions(BHException):
    pass


class UserNotAuthenticated(UserAccountAuthExceptions):

    # The page or resource you were trying to access can not be loaded until
    # you first log-in with a valid username and password.
    STATUS_CODE = 401
    SHOULD_ALERT = False
