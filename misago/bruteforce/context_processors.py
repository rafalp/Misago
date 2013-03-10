def is_jammed(request):
    try:
        return {
            'is_jammed': request.jam.is_jammed(),
        }
    except AttributeError:
        return {}
