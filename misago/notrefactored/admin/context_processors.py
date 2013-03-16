from misago.admin import site

def admin(request):
    return site.get_admin_navigation(request)
