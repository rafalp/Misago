INFO = 'info'
SUCCESS = 'success'
WARNING = 'warning'
ERROR = 'error'

class Messages(object):
    def __init__(self, session):
        self.session = session
        self.messages = session.get('messages_list', [])
        self.session['messages_list'] = []

    def set_message(self, message, level='info', owner=None):
        msg = Message(message)
        msg.level = level
        msg.owner = owner
        self.messages.append(msg)
        return msg

    def set_flash(self, message, level='info', owner=None):
        msg = self.set_message(message, level, owner)
        self.session['messages_list'].append(msg)
        return msg

    def get_message(self, owner=None):
        for index, message in enumerate(self.messages):
            if message.owner == owner:
                del self.messages[index]
                return message
        return None

    def get_messages(self, owner=None):
        orphans = []
        messages = []
        for message in self.messages:
            if message.owner == owner:
                messages.append(message)
            else:
                orphans.append(message)
        self.messages = orphans
        return messages


class Message(object):
    def __init__(self, message=None, level='info', owner=None):
        self.level = level
        self.message = message
        self.owner = owner

    def __unicode__(self):
        return self.message


def get_messages(request, owner=None):
    return request.messages.get_messages(owner)


def add_message(request, level, message, owner=None):
    request.messages.set_flash(unicode(message), level=level, owner=owner)


def info(request, message, owner=None):
    request.messages.set_message(message, level=INFO, owner=owner)


def success(request, message, owner=None):
    request.messages.set_message(message, level=SUCCESS, owner=owner)


def warning(request, message, owner=None):
    request.messages.set_message(message, level=WARNING, owner=owner)


def error(request, message, owner=None):
    request.messages.set_message(message, level=ERROR, owner=owner)