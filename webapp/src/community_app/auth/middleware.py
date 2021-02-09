import logging
from datetime import datetime, timedelta
from typing import Optional

from bh.core_utils.bh_exception import BHException
from bh.services.factory import Factory
from bh_settings import get_settings
from django.conf import settings
from django.contrib.auth import logout

# from django.shortcuts import redirect
from misago.users.models import AnonymousUser

from community_app.constants import COOKIE_NAME_ACCESS_TOKEN, COOKIE_NAME_REFRESH_TOKEN

logger = logging.getLogger("CommunityMiddleware")


class UserNotAuthenticated(BHException):
    # The page or resource you were trying to access can not be loaded until
    # you first log-in with a valid username and password.
    STATUS_CODE = 401
    SHOULD_ALERT = False


class PlatformTokenMiddleware:
    """
    Custom middleware to support coupling Misago/Django user sessions to Platform sessions which are managed with
    access_token and refresh_token cookies

    This is a class-level implementation of the new-style Django middleware (https://docs.djangoproject.com/en/2.2/topics/http/middleware/)
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def _construct_cookie_domain_from_request_headers(self, request_headers: dict) -> Optional[str]:
        """
        Construct a domain string for the cookies from request headers (specifically the host header).

        Args:
            request_headers (dict): the request headers

        Returns:
            Optional[str]: the domain string
        """
        try:
            domain = ".".join(request_headers["host"].split(".")[1:])
            # For local dev, strip port. Is resilient to no port.
            domain = domain.split(":")[0]
            return "." + domain if domain else None
        except KeyError:
            return None

    def _validate_and_refresh_tokens(self, access_token: Optional[str], refresh_token: Optional[str]) -> dict:
        """
        Validates access and/or refresh tokens from Platform

        First, we establish whether we have an authentication entity.
        If we don't, or we don't have an access_token we attempt to refresh our tokens.
        (This allows us to use an existing access_token without a refresh_token)

        If we can't refresh, or we can't obtain an authentication_entity, we raise UserNotAuthenticated

        Args:
            access_token: Platform generated access token
            refresh_token: Platform generated refresh token

        Returns:
            A dict with keys access_token, refresh_token, authentication_entity, cookies_updated
        """
        cookies_updated = False
        authentication_service = None

        authentication_service = Factory.create("UserAccountAuthentication", "1")

        if access_token:
            # This works with either token. If we don't have a refresh token, this means we'll be redirected
            # when it times out.
            authentication_entity = authentication_service.find_with_tokens(access_token=access_token, refresh_token=refresh_token)

        if not access_token or not authentication_entity:
            tokens = authentication_service.refresh_access_token(refresh_token=refresh_token)
            access_token, refresh_token = tokens.get("access_token"), tokens.get("refresh_token")
            authentication_entity = authentication_service.find_with_tokens(access_token=access_token, refresh_token=refresh_token)
            if not authentication_entity:
                raise UserNotAuthenticated
            cookies_updated = True

        return {
            COOKIE_NAME_ACCESS_TOKEN: access_token,
            COOKIE_NAME_REFRESH_TOKEN: refresh_token,
            "authentication_entity": authentication_entity,
            "cookies_updated": cookies_updated,
        }

    def _update_tokens(self, request, response, access_token, refresh_token):
        """
        Updates the response with the latest access_token and refresh_token cookies.
        This follows similar behavior in client-gateway-service-cluster

        Args:
            request: the request
            response: the response
            access_token: the platform access
            refresh_token: the platform refresh_token
        """
        clear_cookie_dt = datetime(year=1970, month=1, day=1)
        domain = self._construct_cookie_domain_from_request_headers(request.headers)
        response.set_cookie(
            COOKIE_NAME_ACCESS_TOKEN,
            access_token,
            expires=(datetime.utcnow() + timedelta(seconds=get_settings("access_token_cookie_expiration_seconds")))
            if access_token
            else clear_cookie_dt,
            domain=domain,
            secure=get_settings("secure_cookies", True),
            httponly=True,
        )

        response.set_cookie(
            COOKIE_NAME_REFRESH_TOKEN,
            refresh_token,
            expires=(datetime.utcnow() + timedelta(days=get_settings("refresh_token_cookie_expiration_days"))) if refresh_token else clear_cookie_dt,
            secure=get_settings("secure_cookies", True),
            domain=domain,
            httponly=True,
        )

    def __call__(self, request):
        """
        Here we validate existence of an authentication entity but ONLY for non-admin users.
        We must support admin users logging in with email, and not using Sleepio auth cookies.
        If we don't have an authentication entity, OR we don't have an access_token (e.g. it's expired)
        we attempt to refresh the tokens with refresh_token

        If that fails, we log the user out and redirect to sleepio (TBD-PENDING)
        If that succeeds, we update the tokens

        It's important that this is placed after Misago's user middleware items in the MIDDLEWARE list in settings.py,
        to ensure we have a user attached to the session, which allows us to log the user off prior to redirecting.

        This is to avoid managing sessions directly, and using built-in behavior to log a user out.

        If we have an authentication entity, we enrich the request to include the platform_user_id, which is used in
        the social_auth_pipeline, fetch_user_account

        Args:
            request (WSGIRequest): The request
        Returns:
            response: The response
        """

        # Code to be executed for each request before
        # the view (and later middleware) are called.
        cookies_updated = False
        authentication_entity = None

        if hasattr(request, "user") and not request.user.is_superuser:
            access_token, refresh_token = request.COOKIES.get(COOKIE_NAME_ACCESS_TOKEN), request.COOKIES.get(COOKIE_NAME_REFRESH_TOKEN)

            try:
                validated_tokens = self._validate_and_refresh_tokens(access_token, refresh_token)
                access_token, refresh_token, authentication_entity, cookies_updated = (
                    validated_tokens.get(COOKIE_NAME_ACCESS_TOKEN),
                    validated_tokens.get(COOKIE_NAME_REFRESH_TOKEN),
                    validated_tokens.get("authentication_entity"),
                    validated_tokens.get("cookies_updated"),
                )
            except BHException as e:
                logger.info(e)
                if settings.SESSION_COOKIE_NAME in request.COOKIES:
                    logout(request)
                    request.user = AnonymousUser()
                # TODO enable this when we have sleepio redirect URLS,
                #   and second level domain cookies working.
                #   Until then, this will always fire upon landing on the page
                #   because we won't have the cookies generated
                # return redirect(get_settings("sleepio_app_url"))

        if authentication_entity:
            request._platform_user_id = authentication_entity.get("user_id")

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        if cookies_updated:
            self._update_tokens(request, response, access_token, refresh_token)

        return response
