from coffin.template import Library
from misago.utils.datesformats import date, reldate, reltimesince

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
