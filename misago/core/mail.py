from django.conf import settings
from django.core import mail as djmail
from django.template import RequestContext
from django.template.loader import render_to_string


def _build_mail(request, recipient, subject, template, context=None):
    context = context or {}
    context['sender'] = request.user
    context['recipient'] = recipient
    context = RequestContext(request, context)

    message_plain = render_to_string('%s.txt' % template, context)
    message_html = render_to_string('%s.html' % template, context)

    message = djmail.EmailMultiAlternatives(subject, message_plain,
                                            to=[recipient.email])
    message.attach_alternative(message_html, "text/html")

    return message


def mail_user(request, recipient, subject, template, context=None):
    message = _build_mail(request, recipient, subject, template, context)
    message.send()


def mail_users(request, recipients, subject, template, context=None, batch=None):
    batch = batch or settings.MISAGO_MAILER_BATCH_SIZE
    messages = []

    for recipient in recipients:
        messages.append(
            _build_mail(request, recipient, subject, template, context))

        if batch and len(messages) >= batch:
            connection = djmail.get_connection()
            connection.send_messages(messages)
            messages = []

    if messages:
        connection = djmail.get_connection()
        connection.send_messages(messages)
