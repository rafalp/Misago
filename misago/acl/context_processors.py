def acl(request):
    return {
        'acl': request.acl,
    }