# pylint: disable=super-init-not-called
class ModerationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
