from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect

from .base import AdminView


class TargetedView(AdminView):
    is_atomic = True

    def check_permissions(self, request, target):
        pass

    def get_target(self, kwargs):
        if len(kwargs) == 1:
            select_for_update = self.get_model().objects
            if self.is_atomic:
                select_for_update = select_for_update.select_for_update()
            # Does not work on Python 3:
            # return select_for_update.get(pk=kwargs[kwargs.keys()[0]])
            (pk, ) = kwargs.values()
            return select_for_update.get(pk=pk)
        else:
            return self.get_model()()

    def get_target_or_none(self, request, kwargs):
        try:
            return self.get_target(kwargs)
        except self.get_model().DoesNotExist:
            return None

    def dispatch(self, request, *args, **kwargs):
        if self.is_atomic:
            with transaction.atomic():
                return self.wrapped_dispatch(request, *args, **kwargs)
        else:
            return self.wrapped_dispatch(request, *args, **kwargs)

    def wrapped_dispatch(self, request, *args, **kwargs):
        target = self.get_target_or_none(request, kwargs)
        if not target:
            messages.error(request, self.message_404)
            return redirect(self.root_link)

        error = self.check_permissions(request, target)
        if error:
            messages.error(request, error)
            return redirect(self.root_link)

        return self.real_dispatch(request, target)

    def real_dispatch(self, request, target):
        pass


class FormView(TargetedView):
    form = None
    template = 'form.html'

    def create_form_type(self, request):
        return self.form

    def initialize_form(self, form, request):
        if request.method == 'POST':
            return form(request.POST, request.FILES)
        else:
            return form()

    def handle_form(self, form, request):
        raise NotImplementedError(
            "You have to define your own handle_form method to handle form submissions."
        )

    def real_dispatch(self, request, target):
        FormType = self.create_form_type(request)
        form = self.initialize_form(FormType, request)

        if request.method == 'POST' and form.is_valid():
            response = self.handle_form(form, request)

            if response:
                return response
            elif 'stay' in request.POST:
                return redirect(request.path)
            else:
                return redirect(self.root_link)

        return self.render(request, {'form': form})


class ModelFormView(FormView):
    message_submit = None

    def create_form_type(self, request, target):
        return self.form

    def initialize_form(self, form, request, target):
        if request.method == 'POST':
            return form(request.POST, request.FILES, instance=target)
        else:
            return form(instance=target)

    def handle_form(self, form, request, target):
        form.instance.save()
        if self.message_submit:
            messages.success(request, self.message_submit % {'name': target.name})

    def real_dispatch(self, request, target):
        FormType = self.create_form_type(request, target)
        form = self.initialize_form(FormType, request, target)

        if request.method == 'POST' and form.is_valid():
            response = self.handle_form(form, request, target)

            if response:
                return response
            elif 'stay' in request.POST:
                return redirect(request.path)
            else:
                return redirect(self.root_link)

        return self.render(request, {'form': form, 'target': target})


class ButtonView(TargetedView):
    def real_dispatch(self, request, target):
        if request.method == 'POST':
            new_response = self.button_action(request, target)
            if new_response:
                return new_response
        return redirect(self.root_link)

    def button_action(self, request, target):
        raise NotImplementedError("You have to define custom button_action.")
