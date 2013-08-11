from django.core.urlresolvers import reverse
from django.shortcuts import redirect

class TypeMixin(object):
    type_prefix = 'report'

    def threads_list_redirect(self):
        return redirect(reverse('reports'))
