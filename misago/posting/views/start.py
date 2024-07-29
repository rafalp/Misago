from django.db import models
from django.http import Http404, HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from ...categories.enums import CategoryTree
from ...categories.models import Category
from ...core.utils import slugify
from ...parser.context import create_parser_context
from ...parser.enums import ContentType, PlainTextFormat
from ...parser.factory import create_parser
from ...parser.html import render_ast_to_html
from ...parser.metadata import create_ast_metadata
from ...parser.plaintext import render_ast_to_plaintext
from ...permissions.categories import check_browse_category_permission
from ...threads.checksums import update_post_checksum
from ...threads.models import Post, Thread
from ..forms.start import ThreadStartForm


class StartView(View):
    template_name: str


class ThreadStartView(StartView):
    template_name: str = "misago/posting/start.html"

    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        category = self.get_category(request, kwargs["id"])
        form = ThreadStartForm()
        return render(
            request,
            self.template_name,
            {"category": category, "form": form},
        )

    def post(self, request: HttpRequest, **kwargs) -> HttpResponse:
        category = self.get_category(request, kwargs["id"])
        form = ThreadStartForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(
                request,
                self.template_name,
                {"category": category, "form": form},
            )

        context = create_parser_context(request, content_type=ContentType.POST)
        parser = create_parser(context)

        ast = parser(form.cleaned_data["post"])
        metadata = create_ast_metadata(context, ast)
        html = render_ast_to_html(context, ast, metadata)
        search_document = (
            form.cleaned_data["title"]
            + " "
            + render_ast_to_plaintext(
                context, ast, metadata, PlainTextFormat.SEARCH_DOCUMENT
            )
        )

        if request.POST.get("preview"):
            return render(
                request,
                self.template_name,
                {
                    "category": category,
                    "form": form,
                    "preview": html,
                    "search_document": search_document,
                },
            )

        now = timezone.now()

        thread = Thread.objects.create(
            category=category,
            title=form.cleaned_data["title"],
            slug=slugify(form.cleaned_data["title"]),
            started_on=now,
            last_post_on=now,
            starter=request.user,
            starter_name=request.user.username,
            starter_slug=request.user.slug,
            last_poster=request.user,
            last_poster_name=request.user.username,
            last_poster_slug=request.user.slug,
        )

        post = Post.objects.create(
            category=category,
            thread=thread,
            poster=request.user,
            poster_name=request.user.username,
            original=form.cleaned_data["post"],
            parsed=html,
            search_document=search_document,
            posted_on=now,
            updated_on=now,
        )

        thread.first_post = post
        thread.last_post = post
        thread.save()

        update_post_checksum(post)
        post.update_search_vector()
        post.save()

        category.threads = models.F("threads") + 1
        category.posts = models.F("posts") + 1
        category.set_last_thread(thread)
        category.save()

        thread_url = reverse(
            "misago:thread",
            kwargs={"pk": thread.id, "slug": thread.slug},
        )

        return redirect(thread_url)

    def get_category(self, request: HttpRequest, category_id: int) -> Category:
        try:
            category = Category.objects.get(
                id=category_id,
                tree_id=CategoryTree.THREADS,
                level__gt=0,
            )
        except Category.DoesNotExist:
            raise Http404()

        check_browse_category_permission(
            request.user_permissions, category, can_delay=True
        )

        return category


class PrivateThreadStartView(StartView):
    pass


def select_category(request: HttpRequest) -> HttpResponse:
    pass
