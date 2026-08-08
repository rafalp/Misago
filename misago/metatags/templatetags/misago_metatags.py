from django import template

register = template.Library()


@register.filter
def mergemetatags(metatags: dict | None = None, default_metatags: dict | None = None):
    if metatags and default_metatags:
        merged = default_metatags.copy()
        merged.update(metatags)
        return remove_empty_metatags(merged).values()

    return remove_empty_metatags(metatags or default_metatags or {}).values()


def remove_empty_metatags(metatags: dict) -> dict:
    return {key: value for key, value in metatags.items() if value}
