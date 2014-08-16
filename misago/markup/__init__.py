# flake8: noqa
from misago.markup.flavours import (common as common_flavour,
                                    limited as limited_flavour,
                                    signature as signature_flavour)
from misago.markup.parser import parse
from misago.markup.editor import Editor


default_app_config = 'misago.markup.apps.MisagoMarkupConfig'
