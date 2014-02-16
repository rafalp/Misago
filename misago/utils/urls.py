#-*- coding: utf-8 -*-
import re
from urlparse import urlparse
from django.conf import settings
from django.core.urlresolvers import resolve
from django.http import Http404
from misago.utils.strings import html_escape

URL_RE = re.compile(r'^(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))$', re.UNICODE)

def is_url(string):
    return URL_RE.search(string.strip()) != None


def is_inner(string):
    try:
        resolve(string.strip())
        return True
    except Http404:
        return False


def clean_inner(string):
    parsed = urlparse(string.strip())
    href = parsed.path
    if parsed.query:
        href += '?%s' % parsed.query
    if parsed.fragment:
        href += '#%s' % parsed.fragment
    return html_escape(href)


def clean_outer(string):
    parsed = urlparse(string.strip())
    if not parsed.scheme:
        return 'http://%s' % string
    return string
