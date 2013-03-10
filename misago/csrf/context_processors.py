def csrf(request):
    try:
        return {
            'csrf_id': request.csrf.csrf_id,
            'csrf_token': request.csrf.csrf_token,
        }
    except AttributeError:
        return {}
