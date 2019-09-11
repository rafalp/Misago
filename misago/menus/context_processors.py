from .models import MenuLink


def navbar(request):
    return {"top_menu_links": MenuLink.objects.get_top_menu_links()}


def footer(request):
    return {"footer_menu_links": MenuLink.objects.get_footer_menu_links()}
