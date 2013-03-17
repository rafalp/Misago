def banning(request):
    try:
        return {
            'is_banned': request.ban.is_banned(),
        }
    except AttributeError:
        return {}
