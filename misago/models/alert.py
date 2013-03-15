from django.db import models
import base64
import cgi
try:
    import cPickle as pickle
except ImportError:
    import pickle

class Alert(models.Model):
    user = models.ForeignKey('User')
    date = models.DateTimeField()
    message = models.TextField()
    variables = models.TextField(null=True, blank=True)

    def vars(self):
        try:
            return pickle.loads(base64.decodestring(self.variables))
        except Exception:
            return {}

    def text(self, var, value):
        value = cgi.escape(value, True)
        try:
            self.vars_raw[var] = value
        except AttributeError:
            self.vars_raw = {var: value}
        return self
    
    def strong(self, var, value):
        try:
            self.vars_raw[var] = '<strong>%s</strong>' % cgi.escape(value, True)
        except AttributeError:
            self.vars_raw = {var: '<strong>%s</strong>' % cgi.escape(value, True)}
        return self

    def url(self, var, value, href, attrs=None):
        url = '<a href="%s"' % cgi.escape(href, True)
        if attrs:
            for k, v in attrs.iterator():
                url += ' %s="%s"' % (k, cgi.escape(v, True))
        url += '>%s</a>' % value
        try:
            self.vars_raw[var] = url
        except AttributeError:
            self.vars_raw = {var: url}
        return self

    def profile(self, var, user):
        from django.core.urlresolvers import reverse
        return self.url(var, user.username, reverse('user', kwargs={'user': user.pk, 'username': user.username_slug}))

    def thread(self, var, thread):
        from django.core.urlresolvers import reverse
        return self.url(var, thread.name, reverse('thread', kwargs={'thread': thread.pk, 'slug': thread.slug}))

    def post(self, var, thread, post):
        from django.core.urlresolvers import reverse
        return self.url(var, thread.name, reverse('thread_find', kwargs={'thread': thread.pk, 'slug': thread.slug, 'post': post.pk}))

    def save_all(self, *args, **kwargs):
        self.save(force_insert=True)
        self.user.save(force_update=True)

    def hydrate(self):
        try:
            self.variables = base64.encodestring(pickle.dumps(self.vars_raw, pickle.HIGHEST_PROTOCOL))
        except AttributeError:
            self.variables = base64.encodestring(pickle.dumps({}, pickle.HIGHEST_PROTOCOL))
        return self

    def save(self, *args, **kwargs):
        self.hydrate()
        super(Alert, self).save(*args, **kwargs)
        return self.user
