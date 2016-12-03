from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class ModerationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
