from django_jinja.library import Library
from misago.utils.datesformats import date, reldate, reltimesince, compact, relcompact

register = Library()


@register.filter(name='date')
def date_filter(val, arg=""):
    return date(val, arg)


@register.filter(name='reldate')
def reldate_filter(val, arg=""):
    return reldate(val, arg)


@register.filter(name='reltimesince')
def reltimesince_filter(val, arg=""):
    return reltimesince(val, arg)


@register.filter(name='compact')
def compact_filter(val):
    return compact(val)


@register.filter(name='relcompact')
def relcompact_filter(val):
    return relcompact(val)