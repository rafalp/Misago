def frontend_context(request):
    if request.include_frontend_context:
        return {
            'frontend_context': request.frontend_context,
        }
    else:
        return {}
