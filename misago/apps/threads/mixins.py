from django.core.urlresolvers import reverse
from django.shortcuts import redirect

class TypeMixin(object):
    templates_prefix = 'threads'
    thread_url = 'thread'

    def threads_list_redirect(self):
        return redirect(reverse('forum', kwargs={'forum': self.forum.pk, 'slug': self.forum.slug}))