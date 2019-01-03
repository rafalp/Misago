from .utils import get_file_hash


def create_css(theme, css):
    order = None
    if css_exists(theme, css):
        order = get_css_order(theme, css)
        delete_css(theme, css)
    save_css(theme, css, order)


def css_exists(theme, css):
    return theme.css.filter(name=css.name).exists()


def get_css_order(theme, css):
    return theme.css.get(name=css.name).order


def delete_css(theme, css):
    theme.css.get(name=css.name).delete()


def save_css(theme, css, order=None):
    if order is None:
        order = get_next_css_order(theme)

    theme.css.create(
        name=css.name,
        source_file=css,
        source_hash=get_file_hash(css),
        size=css.size,
        order=order,
    )


def get_next_css_order(theme):
    last_css = theme.css.order_by("order").last()
    if last_css:
        return last_css.order + 1
    return 0


def move_css_up(theme, css):
    previous_css = theme.css.filter(order__lt=css.order).order_by("-order").first()
    if not previous_css:
        return False

    css.order, previous_css.order = previous_css.order, css.order
    css.save(update_fields=["order"])
    previous_css.save(update_fields=["order"])

    return True


def move_css_down(theme, css):
    next_css = theme.css.filter(order__gt=css.order).order_by("order").first()
    if not next_css:
        return False

    css.order, next_css.order = next_css.order, css.order
    css.save(update_fields=["order"])
    next_css.save(update_fields=["order"])

    return True
