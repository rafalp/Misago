from django.test import override_settings


def disable_parser_clean_ast(f):
    return override_settings(MISAGO_PARSER_CLEAN_AST=False)(f)
