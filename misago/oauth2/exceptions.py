from django.utils.translation import gettext_lazy as _


class OAuth2Error(Exception):
    pass


class OAuth2ProviderError(OAuth2Error):
    pass


class OAuth2AccessDeniedError(OAuth2ProviderError):
    message = _("The OAuth2 process was canceled by the provider.")


class OAuth2StateError(OAuth2Error):
    recoverable = True


class OAuth2StateNotSetError(OAuth2StateError):
    message = _("The OAuth2 session is missing state.")


class OAuth2StateNotProvidedError(OAuth2StateError):
    message = _("The OAuth2 state was not sent by the provider.")


class OAuth2StateMismatchError(OAuth2StateError):
    message = _(
        "The OAuth2 state sent by the provider did not match one in the session."
    )


class OAuth2CodeError(OAuth2Error):
    recoverable = True


class OAuth2CodeNotProvidedError(OAuth2CodeError):
    message = _("The OAuth2 authorization code was not sent by the provider.")


class OAuth2ProviderError(OAuth2Error):
    recoverable = True


class OAuth2AccessTokenRequestError(OAuth2ProviderError):
    message = _("Failed to connect to the OAuth2 provider to retrieve an access token.")


class OAuth2AccessTokenResponseError(OAuth2ProviderError):
    message = _("The OAuth2 provider responded with error for an access token request.")


class OAuth2AccessTokenJSONError(OAuth2ProviderError):
    message = _(
        "The OAuth2 provider did not respond with a valid JSON "
        "for an access token request."
    )


class OAuth2AccessTokenNotProvidedError(OAuth2ProviderError):
    message = _("JSON sent by the OAuth2 provider did not contain an access token.")


class OAuth2UserDataRequestError(OAuth2ProviderError):
    message = _("Failed to connect to the OAuth2 provider to retrieve user profile.")


class OAuth2UserDataResponseError(OAuth2ProviderError):
    message = _("The OAuth2 provider responded with error for user profile request.")


class OAuth2UserDataJSONError(OAuth2ProviderError):
    message = _(
        "The OAuth2 provider did not respond with a valid JSON "
        "for user profile request."
    )


class OAuth2UserIdNotProvidedError(OAuth2Error):
    message = _("JSON sent by the OAuth2 provider did not contain a user id.")


class OAuth2UserAccountDeactivatedError(OAuth2Error):
    recoverable = False
    message = _(
        "User account associated with the profile from the OAuth2 provider was "
        "deactivated by the site administrator."
    )


class OAuth2UserDataValidationError(OAuth2ProviderError):
    recoverable = False
    error_list: list[str]
    message = _("User profile retrieved from the OAuth2 provider did not validate.")

    def __init__(self, error_list: list[str]):
        self.error_list = error_list
