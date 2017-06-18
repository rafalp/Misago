from django.utils.module_loading import import_string
from django.utils.translation import ugettext as _

from misago.conf import settings

from .basefields import *
from .serializers import serialize_profilefields_data


class ProfileFields(object):
    def __init__(self, fields_groups):
        self.is_loaded = False

        self.fields_groups = fields_groups
        self.fields_dict = {}

    def load(self):
        self.fields_dict = {}

        fieldnames = {}

        for group in self.fields_groups:
            for field_path in group['fields']:
                field = import_string(field_path)
                field._field_path = field_path

                if field_path in self.fields_dict:
                    raise ValueError(
                        "{} profile field has been specified twice".format(field._field_path)
                    )

                if not getattr(field, 'fieldname', None):
                    raise ValueError(
                        "{} profile field has to specify fieldname attribute".format(
                            field._field_path,
                        )
                    )

                if field.fieldname in fieldnames:
                    raise ValueError(
                        (
                            '{} profile field defines fieldname "{}" '
                            'that is already in use by the {}'
                        ).format(
                            field._field_path,
                            field.fieldname,
                            fieldnames[field.fieldname],
                        )
                    )

                fieldnames[field.fieldname] = field_path
                self.fields_dict[field_path] = field()

        self.is_loaded = True

    def update_admin_form(self, form):
        if not self.is_loaded:
            self.load()

        for group in self.fields_groups:
            group_dict = {
                'name': _(group['name']),
                'fields': [],
            }

            for field_path in group['fields']:
                field = self.fields_dict[field_path]
                admin_field = field.get_admin_field(form.instance)
                if admin_field:
                    form.fields[field.fieldname] = admin_field
                    group_dict['fields'].append(field.fieldname)

            form._profile_fields_groups.append(group_dict)

    def clean_admin_form(self, form, data):
        for field in self.fields_dict.values():
            data = field.clean_admin_form(form, data) or data
        return data

    def admin_update_profile_fields(self, user, cleaned_data):
        for field in self.fields_dict.values():
            field.admin_update_profile_fields(user, cleaned_data)

    def admin_search(self, criteria, queryset):
        if not self.is_loaded:
            self.load()

        q_obj = None
        for field in self.fields_dict.values():
            q = field.admin_search(criteria, queryset)
            if q:
                if q_obj:
                    q_obj = q_obj | q
                else:
                    q_obj = q
        if q_obj:
            return queryset.filter(q_obj)

        return queryset

    def get_fields(self):
        if not self.is_loaded:
            self.load()
        return self.fields_dict.values()

    def get_fields_groups(self):
        if not self.is_loaded:
            self.load()

        groups = []
        for group in self.fields_groups:
            group_dict = {
                'name': _(group['name']),
                'fields': [],
            }

            for field_path in group['fields']:
                field = self.fields_dict[field_path]
                group_dict['fields'].append(field)

            if group_dict['fields']:
                groups.append(group_dict)
        return groups


profilefields = ProfileFields(settings.MISAGO_PROFILE_FIELDS)
