from misago.views.exceptions import handler


class MisagoExceptionHandlerMiddleware(object):
    def process_exception(self, request, exception):
        if handler.is_misago_exception(exception):
            return handler.handle_misago_exception(request, exception)
        else:
            return None
