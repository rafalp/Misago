from django.shortcuts import *
from misago.views.exceptions import OutdatedSlug


def check_object_slug(model, slug):
    if model.slug != slug:
        raise OutdatedSlug(model)
