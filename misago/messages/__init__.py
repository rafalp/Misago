from coffin.template.loader import select_template

class Message(object):
    """
    Template based mesage used by frontend
    """
    def __init__(self, request, type='base', message=None, extra={}, owner=None):
        self.type = type
        self.message = message
        self.owner = owner
        for key, value in extra.iteritems():
            setattr(self, key, value)
        self.tpl = select_template((
                                    '%s/message/%s.html' % (request.theme.get_theme(), type),
                                    '_message/%s.html' % type,
                                    '%s/message/base.html' % request.theme.get_theme(),
                                    '_message/base.html'
                                    ))
        self.tpl = self.tpl.name
        if self.tpl[9:-5] == 'base':
            self.message = type
            
    def is_basic(self):
        return False


class BasicMessage(object):
    """
    Text based mesage used by ACP
    """
    def __init__(self, message=None, type='info', owner=None):
        self.type = type
        self.message = message
        self.owner = owner
            
    def is_basic(self):
        return True