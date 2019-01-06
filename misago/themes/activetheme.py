from .models import Theme


def get_active_theme():
    active_theme = Theme.objects.get(is_active=True)
    themes = active_theme.get_ancestors(include_self=True)
    themes = themes.prefetch_related("css")

    include_defaults = False
    styles = []

    for theme in themes:
        if theme.is_default:
            include_defaults = True
        for css in theme.css.all():
            if css.url:
                styles.append(css.url)
            elif css.source_needs_building:
                if css.build_file:
                    styles.append(css.build_file.url)
            else:
                styles.append(css.source_file.url)

    return {"include_defaults": include_defaults, "styles": styles}
