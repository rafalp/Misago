from misago import __version__

def misago(request):
    return {
        'version': __version__,
        'monitor': request.monitor,
        'settings': request.settings,
        'stopwatch': request.stopwatch.time(),
    }
