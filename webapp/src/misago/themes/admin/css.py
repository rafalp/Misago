import json
import re

from django.core.files.base import ContentFile

from ...core.utils import get_file_hash


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
        source_needs_building=css_needs_rebuilding(css),
        size=css.size,
        order=order,
    )


def css_needs_rebuilding(css):
    css.seek(0)
    css_source = css.read().decode("utf-8")
    return "url(" in css_source


def get_theme_media_map(theme):
    media_map = {}
    for media in theme.media.all():
        escaped_url = json.dumps(media.file.url)
        media_map[media.name] = escaped_url

        media_filename = str(media.file).split("/")[-1]
        media_map[media_filename] = escaped_url
    return media_map


def rebuild_css(media_map, css):
    if css.build_file:
        css.build_file.delete(save=False)

    css_source = css.source_file.read().decode("utf-8")
    build_source = change_css_source(media_map, css_source).encode("utf-8")

    build_file_name = css.name
    if css.source_hash in build_file_name:
        build_file_name = build_file_name.replace(".%s" % css.source_hash, "")
    build_file = ContentFile(build_source, build_file_name)

    css.build_file = build_file
    css.build_hash = get_file_hash(build_file)
    css.size = len(build_source)
    css.save()


CSS_URL_REGEX = re.compile(r"url\((.+)\)")


def change_css_source(media_map, css_source):
    url_replacer = get_url_replacer(media_map)
    return CSS_URL_REGEX.sub(url_replacer, css_source).strip()


def get_url_replacer(media_map):
    def replacer(matchobj):
        url = matchobj.group(1).strip("\"'").strip()
        if is_url_absolute(url):
            return matchobj.group(0)

        media_name = url.split("/")[-1]
        if media_name in media_map:
            return "url(%s)" % media_map[media_name]

        return matchobj.group(0)

    return replacer


def is_url_absolute(url):
    if url.startswith("//") or url.startswith("://"):
        return True

    if url.lower().startswith("https://"):
        return True

    if url.lower().startswith("http://"):
        return True

    return False


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
