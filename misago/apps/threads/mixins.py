from django.core.urlresolvers import reverse
from django.shortcuts import redirect

class TypeMixin(object):
    type_prefix = 'thread'

    def threads_list_redirect(self):
        return redirect(reverse('forum', kwargs={'forum': self.forum.pk, 'slug': self.forum.slug}))