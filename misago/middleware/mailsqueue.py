from django.conf import settings
from django.core import mail

class MailsQueueMiddleware(object):
    def process_request(self, request):
        request.mails_queue = []

    def process_response(self, request, response):
        try:
            if request.mails_queue:
                connection = mail.get_connection(fail_silently=settings.DEBUG)
                connection.open()
                connection.send_messages(request.mails_queue)
                connection.close()
        except AttributeError:
            pass
        return response