def misago(request):
    return {
        'monitor': request.monitor,
        'settings': request.settings,
        'stopwatch': request.stopwatch.time(),
    }