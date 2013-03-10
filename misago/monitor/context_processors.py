def monitor(request):
    try:
        return {
            'monitor' : request.monitor,
        }
    except AttributeError:
        return {}
