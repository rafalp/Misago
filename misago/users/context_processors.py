def user(request):
    try:
        return {
            'user': request.user,
        }
    except AttributeError:
        pass
