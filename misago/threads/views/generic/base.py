from django.http import Http404
from django.shortcuts import render
from django.views.generic import View

from misago.acl import add_acl
from misago.categories.models import Category
from misago.categories.permissions import (allow_see_category,
                                           allow_browse_category)
from misago.core.shortcuts import get_object_or_404, validate_slug

from misago.threads.models import Thread, Post
from misago.threads.permissions import (allow_see_thread, allow_see_post,
                                        exclude_invisible_posts)


__all__ = ['CategoryMixin', 'ThreadMixin', 'PostMixin', 'ViewBase']


class CategoryMixin(object):
    """
    Mixin for getting categories
    """
    def get_category(self, request, lock=False, **kwargs):
        category = self.fetch_category(request, lock, **kwargs)
        self.check_category_permissions(request, category)

        if kwargs.get('category_slug'):
            validate_slug(category, kwargs.get('category_slug'))

        return category

    def fetch_category(self, request, lock=False, **kwargs):
        queryset = Category.objects
        if lock:
            queryset = queryset.select_for_update()

        return get_object_or_404(
            queryset, id=kwargs.get('category_id'), role='forum')

    def check_category_permissions(self, request, category):
        if category.special_role:
            raise Http404()

        add_acl(request.user, category)
        allow_see_category(request.user, category)
        allow_browse_category(request.user, category)


class ThreadMixin(object):
    """
    Mixin for getting thread
    """
    def get_thread(self, request, lock=False, **kwargs):
        thread = self.fetch_thread(request, lock, **kwargs)
        self.check_thread_permissions(request, thread)

        if kwargs.get('thread_slug'):
            validate_slug(thread, kwargs.get('thread_slug'))

        return thread

    def fetch_thread(self, request, lock=False, select_related=None,
                     queryset=None, **kwargs):
        queryset = queryset or Thread.objects
        if lock:
            queryset = queryset.select_for_update()

        select_related = select_related or []
        if not 'category' in select_related:
            select_related.append('category')
        queryset = queryset.select_related(*select_related)

        where = {'id': kwargs.get('thread_id')}
        if 'category_id' in kwargs:
            where['category_id'] = kwargs.get('category_id')
        return get_object_or_404(queryset, **where)

    def check_thread_permissions(self, request, thread):
        if thread.category.special_role:
            raise Http404()

        add_acl(request.user, thread.category)
        add_acl(request.user, thread)

        allow_see_thread(request.user, thread)
        allow_see_category(request.user, thread.category)


class PostMixin(object):
    def get_post(self, request, lock=False, **kwargs):
        post = self.fetch_post(request, lock, **kwargs)

        post.thread.category = post.category

        self.check_post_permissions(request, post)
        return post

    def fetch_post(self, request, lock=False, select_related=None,
                   queryset=None, **kwargs):
        queryset = queryset or Post.objects
        if lock:
            queryset = queryset.select_for_update()

        select_related = select_related or []
        if not 'category' in select_related:
            select_related.append('category')
        if not 'thread' in select_related:
            select_related.append('thread')
        queryset = queryset.select_related(*select_related)

        where = {'id': kwargs.get('post_id')}
        if 'thread_id' in kwargs:
            where['thread_id'] = kwargs.get('thread_id')
        if 'category_id' in kwargs:
            where['category_id'] = kwargs.get('category_id')

        return get_object_or_404(queryset, **where)

    def check_post_permissions(self, request, post):
        if post.category.special_role:
            raise Http404()

        add_acl(request.user, post.category)
        add_acl(request.user, post.thread)
        add_acl(request.user, post)

        allow_see_post(request.user, post)
        allow_see_thread(request.user, post.thread)
        allow_see_category(request.user, post.category)

    def exclude_invisible_posts(self, queryset, user, category, thread):
        return exclude_invisible_posts(queryset, user, category)


class ViewBase(CategoryMixin, ThreadMixin, PostMixin, View):
    def process_context(self, request, context):
        """
        Simple hook for extending and manipulating template context.
        """
        return context

    def render(self, request, context=None, template=None):
        context = self.process_context(request, context or {})
        template = template or self.template
        return render(request, template, context)
