from misago import __version__

def misago(request):
    try:
        return {
            'version': __version__,
            'monitor': request.monitor,
            'settings': request.settings,
            'stopwatch': request.stopwatch.time(),
        }
    except AttributeError:
        # If request lacks required service, let template crash in context processor's stead
        return  {}
