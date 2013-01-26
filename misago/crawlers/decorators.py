from misago.views import error403

def block_crawlers(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if request.user.is_crawler():
            return error403(request)
        return f(*args, **kwargs)
    return decorator
