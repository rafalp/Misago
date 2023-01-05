from django.utils.translation import gettext_lazy as _


class OAuth2Error(Exception):
    pass


class OAuth2ProviderError(OAuth2Error):
    pass


class OAuth2StateError(OAuth2Error):
    recoverable = True


class OAuth2StateNotSetError(OAuth2StateError):
    message = _("OAuth2 session was missing state.")


class OAuth2StateNotProvidedError(OAuth2StateError):
    message = _("OAuth2 state was not sent by provider.")


class OAuth2StateMismatchError(OAuth2StateError):
    message = _("OAuth2 state sent by provider did not match one in the session.")


class OAuth2CodeError(OAuth2Error):
    recoverable = True


class OAuth2CodeNotProvidedError(OAuth2CodeError):
    message = _("OAuth2 authorization code was not sent by provider.")


class OAuth2ProviderError(OAuth2Error):
    recoverable = True


class OAuth2AccessTokenRequestError(OAuth2ProviderError):
    message = _("Failed to connect to OAuth2 provider to retrieve access token.")


class OAuth2AccessTokenResponseError(OAuth2ProviderError):
    message = _("OAuth2 provider responded with error for access token request.")


class OAuth2AccessTokenJSONError(OAuth2ProviderError):
    message = _(
        "OAuth2 provider did not respond with a valid JSON for access token request."
    )


class OAuth2AccessTokenNotProvidedError(OAuth2ProviderError):
    message = _("JSON sent by OAuth2 provider did not contain an access token.")


class OAuth2UserDataRequestError(OAuth2ProviderError):
    message = _("Failed to connect to OAuth2 provider to retrieve user profile.")


class OAuth2UserDataResponseError(OAuth2ProviderError):
    message = _("OAuth2 provider responded with error for user profile request.")


class OAuth2UserDataJSONError(OAuth2ProviderError):
    message = _(
        "OAuth2 provider did not respond with a valid JSON for user profile request."
    )


class OAuth2UserIdNotProvidedError(OAuth2Error):
    message = _("JSON sent by OAuth2 provider did not contain a user id.")
