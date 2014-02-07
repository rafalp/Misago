from django.shortcuts import *
from misago.core.exceptions import OutdatedSlug


def validate_slug(model, slug):
    if model.slug != slug:
        raise OutdatedSlug(model)
