from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect

from misago.threads.viewmodels import ForumThread, PrivateThread, ThreadPost, ThreadsCategory

from .models import OldIdRedirect


UserModel = get_user_model()


def category_redirect(request, **kwargs):
    category_pk = get_new_id_or_404(OldIdRedirect.CATEGORY, kwargs['forum'])
    category = ThreadsCategory(request, pk=category_pk)
    return redirect(category.get_absolute_url(), permanent=True)


def thread_redirect(request, **kwargs):
    thread_pk = get_new_id_or_404(OldIdRedirect.THREAD, kwargs['thread'])
    thread = ForumThread(request, pk=thread_pk)

    if 'post' in kwargs:
        post_pk = get_new_id_or_404(OldIdRedirect.POST, kwargs['post'])
        post = ThreadPost(request, thread, pk=post_pk)
        return redirect(post.get_absolute_url(), permanent=True)

    return redirect(thread.get_absolute_url(), permanent=True)


def private_thread_redirect(request, **kwargs):
    thread_pk = get_new_id_or_404(OldIdRedirect.THREAD, kwargs['thread'])
    thread = PrivateThread(request, pk=thread_pk)

    if 'post' in kwargs:
        post_pk = get_new_id_or_404(OldIdRedirect.POST, kwargs['post'])
        post = ThreadPost(request, thread, pk=post_pk)
        return redirect(post.get_absolute_url(), permanent=True)

    return redirect(thread.get_absolute_url(), permanent=True)


def user_redirect(request, **kwargs):
    user_pk = get_new_id_or_404(OldIdRedirect.USER, kwargs['user'])
    user = get_object_or_404(UserModel, pk=user_pk)

    return redirect(user.get_absolute_url(), permanent=True)


def get_new_id_or_404(model, old_id):
    return get_object_or_404(OldIdRedirect, model=model, old_id=old_id).new_id
