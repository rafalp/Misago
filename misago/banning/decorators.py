from misago.banning.views import error_banned

def block_banned(f):
    def decorator(*args, **kwargs):
        request = args[0]
        try:
            if request.user.is_banned() or request.ban.is_banned():
                return error_banned(request);
            return f(*args, **kwargs)
        except AttributeError:
            pass
        return f(*args, **kwargs)
    return decorator