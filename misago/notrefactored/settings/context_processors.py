def settings(request):
    try:
        return {
            'settings' : request.settings,
        }
    except AttributeError:
        return {}
