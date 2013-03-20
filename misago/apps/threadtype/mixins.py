from django import forms
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ungettext
from misago.utils.strings import slugify
from misago.utils.pagination import make_pagination

class ValidateThreadNameMixin(object):
    def clean_thread_name(self):
        data = self.cleaned_data['thread_name']
        slug = slugify(data)
        if len(slug) < self.request.settings['thread_name_min']:
            raise forms.ValidationError(ungettext(
                                                  "Thread name must contain at least one alpha-numeric character.",
                                                  "Thread name must contain at least %(count)d alpha-numeric characters.",
                                                  self.request.settings['thread_name_min']
                                                  ) % {'count': self.request.settings['thread_name_min']})
        if len(data) > self.request.settings['thread_name_max']:
            raise forms.ValidationError(ungettext(
                                                  "Thread name cannot be longer than %(count)d character.",
                                                  "Thread name cannot be longer than %(count)d characters.",
                                                  self.request.settings['thread_name_max']
                                                  ) % {'count': self.request.settings['thread_name_max']})
        return data


class RedirectToPostMixin(object):
    def _redirect_to_post(self, link, post):
        pagination = make_pagination(0, self.request.acl.threads.filter_posts(self.request, self.thread, self.thread.post_set).filter(id__lte=post.pk).count(), self.request.settings.posts_per_page)
        if pagination['total'] > 1:
            return redirect(reverse(link, kwargs={'thread': self.thread.pk, 'slug': self.thread.slug, 'page': pagination['total']}) + ('#post-%s' % post.pk))
        return redirect(reverse(link, kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % post.pk))
