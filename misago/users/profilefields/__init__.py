from django.utils.module_loading import import_string

from misago.conf import settings

from .base import ProfileField, TextProfileField


class ProfileFields(object):
    def __init__(self, fields_groups):
        self.is_loaded = False

        self.fields_groups = fields_groups
        self.fields_dict = {}

    def load(self):
        self.fields_dict = {}

        for group in self.fields_groups:
            for field_path in group['fields']:
                field = import_string(field_path)
                field._field_path = field_path
                if not field.fieldname:
                    raise ValueError(
                        "{} profile field has to specify fieldname attribute".format(
                            field._field_path,
                        )
                    )
                if field.fieldname in self.fields_dict:
                    raise ValueError(
                        (
                            '{} profile field defines fieldname "{}" '
                            'that is already in use by the {}'
                        ).format(
                            field._field_path,
                            field.fieldname,
                            dict_from_map[field.fieldname]._field_path,
                        )
                    )
                self.fields_dict[field_path] = field

        self.is_loaded = True

    def extend_admin_form(self, form, user):
        class ProfileFieldsForm(form, ProfileFieldsMixin):
            profile_fields_groups = []

        new_form = ProfileFieldsForm

        if not self.is_loaded:
            self.load()

        for group in self.fields_groups:
            group_dict = {
                'name': group['name'],
                'fields': [],
            }

            for field_path in group['fields']:
                old_form = new_form

                field = self.fields_dict[field_path]()
                new_form = field.extend_admin_form(old_form, user)

                if new_form != old_form:
                   group_dict['fields'].append(field.fieldname)

            if group_dict['fields']:
                new_form.profile_fields_groups.append(group_dict)

        return new_form


class ProfileFieldsMixin(object):
    def get_profile_fields_groups(self):
        profile_fields_groups = []
        for group in self.profile_fields_groups:
            fields_group = {
                'name': group['name'],
                'fields': [],
            }

            for fieldname in group['fields']:
                fields_group['fields'].append(self[fieldname])

            profile_fields_groups.append(fields_group)
        return profile_fields_groups


profilefields = ProfileFields(settings.MISAGO_PROFILE_FIELDS)
