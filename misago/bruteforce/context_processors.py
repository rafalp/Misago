def is_jammed(request):
    if request.user.is_crawler():
        return {}
    return {
        'is_jammed': request.jam.is_jammed(),
    }
