from django.core import mail as djmail
from django.template.loader import render_to_string


def build_mail(request, recipient, subject, template, context=None):
    context = context or {}
    context['sender'] = request.user
    context['recipient'] = recipient
    context['subject'] = subject

    message_plain = render_to_string('%s.txt' % template, context, request=request)
    message_html = render_to_string('%s.html' % template, context, request=request)

    message = djmail.EmailMultiAlternatives(subject, message_plain, to=[recipient.email])
    message.attach_alternative(message_html, "text/html")

    return message


def mail_user(request, recipient, subject, template, context=None):
    message = build_mail(request, recipient, subject, template, context)
    message.send()


def mail_users(request, recipients, subject, template, context=None):
    messages = []

    for recipient in recipients:
        messages.append(build_mail(request, recipient, subject, template, context))

    if messages:
        send_messages(messages)


def send_messages(messages):
    connection = djmail.get_connection()
    connection.send_messages(messages)
