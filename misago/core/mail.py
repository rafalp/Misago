from django.core import mail as djmail
from django.template.loader import render_to_string
from django.utils.translation import get_language

from ..conf import settings
from .utils import get_host_from_address


def build_mail(recipient, subject, template, sender=None, context=None):
    context = context.copy() if context else {}
    if not context.get("settings"):
        raise ValueError("settings key is missing from context")

    forum_address = context["settings"].forum_address

    context.update(
        {
            "LANGUAGE_CODE": get_language()[:2],
            "LOGIN_URL": settings.LOGIN_URL,
            "forum_host": get_host_from_address(forum_address),
            "user": recipient,
            "sender": sender,
            "subject": subject,
        }
    )

    message_plain = render_to_string("%s.txt" % template, context)
    message_html = render_to_string("%s.html" % template, context)

    message = djmail.EmailMultiAlternatives(
        subject, message_plain, to=[recipient.email]
    )
    message.attach_alternative(message_html, "text/html")

    return message


def mail_user(recipient, subject, template, sender=None, context=None):
    message = build_mail(recipient, subject, template, sender, context)
    message.send()


def mail_users(recipients, subject, template, sender=None, context=None):
    messages = []

    for recipient in recipients:
        messages.append(build_mail(recipient, subject, template, sender, context))

    if messages:
        send_messages(messages)


def send_messages(messages):
    connection = djmail.get_connection()
    connection.send_messages(messages)
