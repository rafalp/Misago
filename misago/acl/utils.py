from misago.views import error403, error404

class ACLError403(Exception):
    pass

class ACLError404(Exception):
    pass

def acl_errors(f):
    def decorator(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ACLError403 as e:
            return error403(args[0], e.message)
        except ACLError404 as e:
            return error404(args[0], e.message)
    return decorator