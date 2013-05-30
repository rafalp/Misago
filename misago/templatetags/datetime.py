from coffin.template import Library
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
def compact_filter(val, arg=""):
    return compact(val, arg)


@register.filter(name='relcompact')
def relcompact_filter(val, arg=""):
    return relcompact(val, arg)