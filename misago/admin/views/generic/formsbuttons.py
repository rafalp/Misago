from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect

from .base import AdminView


class TargetedView(AdminView):
    is_atomic = True

    def dispatch(self, request, *args, **kwargs):
        if self.is_atomic:
            with transaction.atomic():
                return self.wrapped_dispatch(request, *args, **kwargs)
        return self.wrapped_dispatch(request, *args, **kwargs)

    def wrapped_dispatch(self, request, *args, **kwargs):
        target = self.get_target_or_none(request, kwargs)
        if not target:
            messages.error(request, self.message_404)
            return redirect(self.root_link)

        error = self.check_permissions(  # pylint: disable=assignment-from-no-return
            request, target
        )
        if error:
            messages.error(request, error)
            return redirect(self.root_link)

        return self.real_dispatch(request, target)

    def get_target_or_none(self, request, kwargs):
        try:
            return self.get_target(kwargs)
        except self.get_model().DoesNotExist:
            return None

    def get_target(self, kwargs):
        if len(kwargs) > 1:
            raise ValueError("TargetedView.get_target() received more than one kwarg")
        if len(kwargs) != 1:
            return self.get_model()()

        queryset = self.get_model().objects
        if self.is_atomic:
            queryset = queryset.select_for_update()
        (pk,) = kwargs.values()
        return queryset.get(pk=pk)

    def check_permissions(self, request, target):
        pass

    def real_dispatch(self, request, target):
        pass


class FormView(TargetedView):
    form_class = None
    template_name = "form.html"

    def get_form_class(self, request):
        return self.form_class

    def get_form(self, form_class, request):
        if request.method == "POST":
            return form_class(request.POST, request.FILES)
        return form_class()

    def handle_form(self, form, request):
        raise NotImplementedError(
            "You have to define your own handle_form method to handle form submissions."
        )

    def real_dispatch(self, request, target):
        FormType = self.get_form_class(request)
        form = self.get_form(FormType, request)

        if request.method == "POST" and form.is_valid():
            response = self.handle_form(form, request)

            if response:
                return response
            if "stay" in request.POST:
                return redirect(request.path)
            return redirect(self.root_link)

        return self.render(request, {"form": form})


class ModelFormView(FormView):
    message_submit = None

    def get_form_class(self, request, target):
        return self.form_class

    def get_form(self, form_class, request, target):
        if request.method == "POST":
            return form_class(request.POST, request.FILES, instance=target)
        return form_class(instance=target)

    def handle_form(self, form, request, target):
        form.instance.save()
        if self.message_submit:
            messages.success(request, self.message_submit % {"name": target.name})

    def real_dispatch(self, request, target):
        form_class = self.get_form_class(request, target)
        form = self.get_form(form_class, request, target)

        if request.method == "POST" and form.is_valid():
            response = self.handle_form(  # pylint: disable=assignment-from-no-return
                form, request, target
            )
            if response:
                return response
            if "stay" in request.POST:
                return redirect(request.path)
            return redirect(self.root_link)

        template_name = self.get_template_name(request, target)
        return self.render(request, {"form": form, "target": target}, template_name)

    def get_template_name(self, request, target):
        return "%s/%s" % (self.templates_dir, self.template_name)


class ButtonView(TargetedView):
    def real_dispatch(self, request, target):
        if request.method == "POST":
            new_response = self.button_action(request, target)
            if new_response:
                return new_response
        return redirect(self.root_link)

    def button_action(self, request, target):
        raise NotImplementedError("You have to define custom button_action.")
