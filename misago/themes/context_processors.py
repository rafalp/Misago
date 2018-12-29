from .models import Theme


def theme(request):
    active_theme = Theme.objects.get(is_active=True)
    themes = active_theme.get_ancestors(include_self=True)
    themes = themes.prefetch_related("css")

    include_defaults = False
    styles = []

    for theme in themes:
        if theme.is_default:
            include_defaults = True
        for css in theme.css.all():
            styles.append(css.file.url)

    return {"theme": {"include_defaults": include_defaults, "styles": styles}}
