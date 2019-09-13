from .menu_links import get_top_menu_links, get_footer_menu_links


def navbar(request):
    return {"top_menu_links": get_top_menu_links(request.cache_versions)}


def footer(request):
    return {"footer_menu_links": get_footer_menu_links(request.cache_versions)}
