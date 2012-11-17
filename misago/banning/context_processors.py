def banning(request):
    if request.user.is_crawler():
        return {}
    return {
        'is_banned': request.ban.is_banned(),
    }