def block_banned(f):
    def decorator(*args, **kwargs):
        request = args[0]
        try:
            if request.ban.is_banned():
                from misago.banning.views import error_banned
                return error_banned(request);
            return f(*args, **kwargs)
        except AttributeError:
            pass
        return f(*args, **kwargs)
    return decorator
