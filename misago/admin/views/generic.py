from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import View
from misago.admin import site
from misago.admin.views import render


class AdminBaseMixin(object):
    """
    Admin mixin abstraciton used for configuring admin CRUD views.

    Takes following attributes:

    Model = Model instance
    message_404 = string used in "requested item not found" messages
    root_link = name of link leading to root action (eg. list of all items
    template_dir = directory with templates
    """
    Model = None
    message_404 = None
    root_link = None
    template_dir = None

    def get_model(self):
        return self.Model


class AdminView(View):
    def final_template(self):
        return '%s/%s' % (self.template_dir, self.template)

    def get_target(self, target):
        Model = self.get_model()
        return Model.objects.get(id=target)

    def _get_target(self, request, kwargs):
        """
        get_target is called by view to fetch item from DB
        """
        Model = self.get_model()

        try:
            return self.get_target(target)
        except Model.DoesNotExist:
            messages.error(request, self.message_404)
            return redirect(self.root_link)

    def render(self, request, context=None):
        context = context or {}
        return render(request, self.final_template(), context)


class ItemsList(AdminView):
    template = 'list.html'

    items_per_page = 0

    def dispatch(self, request, *args, **kwargs):
        context = {}

        context['items'] = self.get_model().objects.all()

        return self.render(request, context)


class FormView(AdminView):
    template = 'form.html'

    def dispatch(self, request, *args, **kwargs):
        pass


class ButtonView(AdminView):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
