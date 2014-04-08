from django.shortcuts import *  # noqa


def paginate(object_list, page, per_page, orphans=0,
             allow_empty_first_page=True):
    from django.http import Http404
    from django.core.paginator import Paginator, EmptyPage
    from misago.core.exceptions import ExplicitFirstPage

    if page in (1, "1"):
        raise ExplicitFirstPage()
    elif not page:
        page = 1

    try:
        return Paginator(
            object_list, per_page, orphans=orphans,
            allow_empty_first_page=allow_empty_first_page).page(page)
    except EmptyPage:
        raise Http404()


def validate_slug(model, slug):
    from misago.core.exceptions import OutdatedSlug
    if model.slug != slug:
        raise OutdatedSlug(model)
