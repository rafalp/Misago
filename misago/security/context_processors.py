def security(request):
    if request.user.is_crawler():
        return {}
    return {
        'csrf_id': request.csrf.csrf_id,
        'csrf_token': request.csrf.csrf_token,
        'is_jammed': request.jam.is_jammed(),
    }