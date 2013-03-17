def acl(request):
    try:
        return {
            'acl': request.acl,
        }
    except AttributeError:
        pass
