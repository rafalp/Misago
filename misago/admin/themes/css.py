from .utils import get_file_hash


def create_css(theme, css):
    if css_exists(theme, css):
        delete_css(theme, css)
    save_css(theme, css)


def css_exists(theme, css):
    return theme.css.filter(name=css.name).exists()


def delete_css(theme, css):
    theme.css.get(name=css.name).delete()


def save_css(theme, css):
    theme.css.create(
        name=css.name, source_file=css, source_hash=get_file_hash(css), size=css.size
    )
