class ModerationError(Exception):
    def __init__(self, message):
        self.message = message

    def __unicode__(self):
        return self.message
