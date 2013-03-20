from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from itertools import chain
from misago.apps.forumbase.mixins import RedirectToPostMixin
from misago.apps.forumbase.posting import PostingBaseView
from misago.markdown import post_markdown
from misago.messages import Message
from misago.models import Forum, Thread, Post
from misago.utils.strings import slugify
from misago.apps.threads.forms import NewThreadForm
from misago.apps.threads.mixins import TypeMixin

class NewReplyView(PostingBaseView, TypeMixin, RedirectToPostMixin):
    pass