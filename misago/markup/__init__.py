# flake8: noqa
from .flavours import common as common_flavour, signature as signature_flavour
from .parser import parse
from .editor import Editor


default_app_config = 'misago.markup.apps.MisagoMarkupConfig'
