from .activetheme import get_active_theme
from .cache import get_theme_cache, set_theme_cache


def theme(request):
    active_theme = get_theme_cache(request.cache_versions)
    if active_theme is None:
        active_theme = get_active_theme()
        set_theme_cache(request.cache_versions, active_theme)

    return {"theme": active_theme}
