from rest_framework.response import Response

from django import forms


from misago.users.profilefields import profilefields, serialize_profilefields_data


def edit_details_endpoint(request, user):
    if request.method == 'GET':
        return get_form_description(request, user)

    return submit_form(request, user)


def get_form_description(request, user):
    groups = []
    for group in profilefields.get_fields_groups():
        group_fields = []
        for field in group['fields']:
            if field.can_edit(request, user):
                group_fields.append(field.get_edit_field_json(request, user))
        if group_fields:
            groups.append({
                'name': group['name'],
                'fields': group_fields
            })

    return Response(groups)


def submit_form(request, user):
    fields = []
    for field in profilefields.get_fields():
        if field.can_edit(request, user):
            fields.append(field)

    form = DetailsForm(
        request.data,
        request=request,
        user=user,
        profilefields=fields,
    )

    if form.is_valid():
        user.profile_fields = form.cleaned_data
        user.save(update_fields=['profile_fields'])

        return Response(serialize_profilefields_data(request, profilefields, user))

    return Response(form.errors, status=400)


class DetailsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.user = kwargs.pop('user')
        self.profilefields = kwargs.pop('profilefields')

        super(DetailsForm, self).__init__(*args, **kwargs)

        for field in self.profilefields:
            self.fields[field.fieldname] = field.get_field_for_validation(
                self.request, self.user)

    def clean(self):
        data = super(DetailsForm, self).clean()
        for field in self.profilefields:
            if field.fieldname in data:
                try:
                    data[field.fieldname] = field.clean_field(
                        self.request, self.user, data[field.fieldname])
                except forms.ValidationError as e:
                    self.add_error(field.fieldname, e)
        return data
