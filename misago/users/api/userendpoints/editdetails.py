from django import forms
from rest_framework.response import Response

from ...profilefields import profilefields, serialize_profilefields_data


def edit_details_endpoint(request, user):
    if request.method == "GET":
        return get_form_description(request, user)

    return submit_form(request, user)


def get_form_description(request, user):
    groups = []
    for group in profilefields.get_fields_groups():
        group_fields = []
        for field in group["fields"]:
            if field.is_editable(request, user):
                group_fields.append(field.get_form_field_json(request, user))
        if group_fields:
            groups.append({"name": group["name"], "fields": group_fields})

    return Response(groups)


def submit_form(request, user):
    fields = []
    for field in profilefields.get_fields():
        if field.is_editable(request, user):
            fields.append(field)

    form = DetailsForm(request.data, request=request, user=user)

    if form.is_valid():
        profilefields.update_user_profile_fields(request, user, form)
        user.save(update_fields=["profile_fields"])

        return Response(serialize_profilefields_data(request, profilefields, user))

    return Response(form.errors, status=400)


class DetailsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.user = kwargs.pop("user")

        super().__init__(*args, **kwargs)

        profilefields.add_fields_to_form(self.request, self.user, self)

    def clean(self):
        data = super().clean()
        return profilefields.clean_form(self.request, self.user, self, data)
