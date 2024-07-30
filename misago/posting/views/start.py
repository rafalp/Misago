from django.db import models
from django.forms import Form
from django.http import Http404, HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from ...categories.enums import CategoryTree
from ...categories.models import Category
from ...core.utils import slugify
from ...parser.context import ParserContext, create_parser_context
from ...parser.enums import ContentType, PlainTextFormat
from ...parser.factory import create_parser
from ...parser.html import render_ast_to_html
from ...parser.metadata import create_ast_metadata
from ...parser.plaintext import render_ast_to_plaintext
from ...permissions.enums import CategoryPermission
from ...permissions.categories import check_browse_category_permission
from ...threads.checksums import update_post_checksum
from ...threads.models import Post, Thread
from ..forms.start import ThreadStartForm


class StartView(View):
    template_name: str
    form_class = ThreadStartForm

    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        category = self.get_category(request, kwargs["id"])
        form = ThreadStartForm()

        return render(
            request,
            self.template_name,
            self.get_context(request, category, form),
        )

    def post(self, request: HttpRequest, **kwargs) -> HttpResponse:
        category = self.get_category(request, kwargs["id"])
        form = ThreadStartForm(request.POST, request.FILES)

        if not form.is_valid():
            return render(
                request,
                self.template_name,
                self.get_context(request, category, form),
            )

        if request.POST.get("preview"):
            context = self.get_context(request, category, form)
            context["preview"] = self.get_preview(request, form)

            return render(request, self.template_name, context)

        thread = self.create_thread(request, category, form)
        thread_url = self.get_thread_url(request, thread)
        return redirect(thread_url)

    def get_form(self, request: HttpRequest, category: Category) -> Form:
        if request.method == "POST":
            return self.form_class(request.POST, request.FILES)

        return self.form_class()

    def get_context(self, request: HttpRequest, category: Category, form: Form) -> dict:
        return {"category": category, "form": form}

    def get_preview(self, request: HttpRequest, form: Form) -> str:
        context, ast, metadata = self.parse_post(request, form)
        return render_ast_to_html(context, ast, metadata)

    def create_thread(
        self, request: HttpRequest, category: Category, form: Form
    ) -> Thread:
        raise NotImplementedError()

    def parse_post(
        self, request: HttpRequest, form: Form
    ) -> tuple[ParserContext, list[dict], dict]:
        context = create_parser_context(request, content_type=ContentType.POST)
        parser = create_parser(context)
        ast = parser(form.cleaned_data["post"])
        metadata = create_ast_metadata(context, ast)
        return context, ast, metadata

    def get_thread_url(self, request: HttpRequest, thread: Thread) -> str:
        raise NotImplementedError()


class ThreadStartView(StartView):
    template_name: str = "misago/posting/start.html"

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

    def create_thread(
        self, request: HttpRequest, category: Category, form: Form
    ) -> Thread:
        context, ast, metadata = self.parse_post(request, form)

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

        html = render_ast_to_html(context, ast, metadata)
        search = render_ast_to_plaintext(
            context, ast, metadata, text_format=PlainTextFormat.SEARCH_DOCUMENT
        )

        post = Post.objects.create(
            category=category,
            thread=thread,
            poster=request.user,
            poster_name=request.user.username,
            original=form.cleaned_data["post"],
            parsed=html,
            search_document=search,
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

        return thread

    def get_thread_url(self, request: HttpRequest, thread: Thread) -> str:
        return reverse(
            "misago:thread",
            kwargs={"pk": thread.id, "slug": thread.slug},
        )


class PrivateThreadStartView(StartView):
    pass


class ThreadStartSelectCategoryView(View):
    template_name = "misago/posting/select_category_page.html"
    template_name_htmx = "misago/posting/select_category_modal.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        context = self.get_context(request)

        if request.is_htmx:
            template_name = self.template_name_htmx
        else:
            template_name = self.template_name

        return render(request, template_name, context)

    def get_context(self, request: HttpRequest) -> dict:
        permissions = request.user_permissions.categories[CategoryPermission.START]

        choices: list[dict] = []
        for category in request.categories.categories_list:
            choice = {
                "id": category["id"],
                "name": category["name"],
                "slug": category["slug"],
                "color": category["color"],
                "level": "",
                "is_vanilla": category["is_vanilla"],
                "disabled": (
                    category["is_vanilla"] or category["id"] not in permissions
                ),
            }

            if not category["level"]:
                choice["children"] = []
                choices.append(choice)
            else:
                parent = choices[-1]
                choice["level"] = "1" * (category["level"] - 1)
                parent["children"].append(choice)

        # Remove branches where entire branch is disabled
        clean_choices: list[dict] = []
        for category in choices:
            clean_children: list[dict] = []
            for child in reversed(category["children"]):
                if not child["disabled"] or (
                    clean_children and clean_children[-1]["level"] > child["level"]
                ):
                    clean_children.append(child)

            if not category["disabled"] or clean_children:
                category["children"] = reversed(clean_children)
                clean_choices.append(category)

        return {"start_thread_choices": clean_choices}
