import logging

from django.shortcuts import redirect
from django.urls import reverse

from bh.services.factory import Factory

from misago.socialauth.pipeline import perpare_username

logger = logging.getLogger("CommunityPipeline")


def fetch_user_account(request, *args, **kwargs) -> dict:
    if hasattr(request, "_platform_user_id"):
        user_account_entity = Factory.create("UserAccount", "1").read(entity_id=request._platform_user_id)
        return dict(user_account=user_account_entity)
    else:
        logger.debug("Middleware did not supply _platform_user_id. Redirecting to Sleepio...")
        return redirect(reverse('social:begin', args=(["sleepio"])))


def get_username(details, *args, **kwargs) -> dict:
    return {"clean_username": perpare_username(details["username"])}


def social_details(backend, user_account, details, *args, **kwargs):
    return {"details": dict(backend.get_user_details(user_account), **details)}
