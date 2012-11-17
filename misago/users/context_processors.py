def user(request):
    return {
        'user': request.user,
    }