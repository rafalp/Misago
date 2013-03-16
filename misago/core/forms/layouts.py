from UserDict import IterableUserDict
from django.utils import formats

class FormLayout(object):
    """
    Conglomelate of fields and fieldsets describing form structure
    """
    def __init__(self, form, fieldsets=False):
        scaffold_fields = FormFields(form)
        scaffold_fieldsets = FormFieldsets(form, scaffold_fields.fields, fieldsets)

        self.multipart_form = scaffold_fields.multipart_form
        self.fieldsets = scaffold_fieldsets.fieldsets
        self.fields = scaffold_fields.fields
        self.hidden = scaffold_fields.hidden


class FormFields(object):
    """
    Hydrator that builds fields list from form and blueprint
    """
    def __init__(self, form):
        self.multipart_form = False
        self.fields = {}
        self.hidden = []

        # Extract widgets from meta
        self.meta_widgets = {}
        try:
            self.meta_widgets = form.Meta.widgets
        except AttributeError:
            pass

        # Find out field input types
        for field in form.fields.keys():
            widget = self._get_widget(field, form.fields[field])
            widget_name = widget.__class__.__name__
            bound_field = form[field]
            blueprint = {
                         'attrs': {
                                    'id': bound_field.auto_id,
                                    'name': bound_field.html_name,
                                   },
                         'endrow': False,
                         'errors': [],
                         'has_value': bound_field.value() != None,
                         'help_text': bound_field.help_text,
                         'hidden': widget.is_hidden,
                         'html_id': bound_field.auto_id,
                         'html_name': bound_field.html_name,
                         'id': field,
                         'initial': bound_field.field.initial,
                         'label': bound_field.label,
                         'last': False,
                         'nested': [],
                         'required': bound_field.field.widget.is_required,
                         'show_hidden_initial': bound_field.field.show_hidden_initial,
                         'value': bound_field.value(),
                         'width': 100,
                         'widget': '',
                         'choices': [],
                        }

            # Set multipart form
            if widget.needs_multipart_form:
                self.multipart_form = True

            # Get errors?
            if form.is_bound:
                for error in bound_field._errors():
                    blueprint['errors'].append(error)
                try:
                    for error in form.errors[field]:
                        if not error in blueprint['errors']:
                            blueprint['errors'].append(error)
                except KeyError:
                    pass

            # Use clean value instead?
            try:
                if field in form.cleaned_data:
                    blueprint['value'] = form.cleaned_data[field]
            except AttributeError:
                pass

            # TextInput
            if widget_name in ['TextInput', 'PasswordInput', 'Textarea']:
                blueprint['widget'] = 'text'
                blueprint['attrs']['type'] = 'text'
                try:
                    blueprint['attrs']['maxlength'] = bound_field.field.max_length
                except AttributeError:
                    pass

            # PasswordInput
            if widget_name == 'PasswordInput':
                blueprint['attrs']['type'] = 'password'

            # Textarea      
            if widget_name == 'Textarea':
                blueprint['widget'] = 'textarea'

            # ReCaptcha      
            if widget_name == 'ReCaptchaWidget':
                from recaptcha.client.captcha import displayhtml
                blueprint['widget'] = 'recaptcha'
                blueprint['attrs'] = {'html': displayhtml(
                                                          form.request.settings['recaptcha_public'],
                                                          form.request.settings['recaptcha_ssl'],
                                                          bound_field.field.api_error,
                                                          )}

            # HiddenInput
            if widget_name == 'HiddenInput':
                blueprint['widget'] = 'hidden'

            # MultipleHiddenInput
            if widget_name == 'MultipleHiddenInput':
                blueprint['widget'] = 'multiple_hidden'
                blueprint['attrs'] = {
                                      'choices': widget.choices
                                     }

            # FileInput
            if widget_name == 'FileInput':
                blueprint['widget'] = 'file'

            # ClearableFileInput
            if widget_name == 'ClearableFileInput':
                blueprint['widget'] = 'file_clearable'

            # DateInput
            if widget_name == 'DateInput':
                blueprint['widget'] = 'date'
                try:
                    blueprint['value'] = blueprint['value'].strftime('%Y-%m-%d')
                except AttributeError as e:
                    pass

            # DateTimeInput
            if widget_name == 'DateTimeInput':
                blueprint['widget'] = 'datetime'
                try:
                    blueprint['value'] = blueprint['value'].strftime('%Y-%m-%d %H:%M')
                except AttributeError as e:
                    pass

            # TimeInput
            if widget_name == 'TimeInput':
                blueprint['widget'] = 'time'
                try:
                    blueprint['value'] = blueprint['value'].strftime('%H:%M')
                except AttributeError as e:
                    pass

            # CheckboxInput
            if widget_name == 'CheckboxInput':
                blueprint['widget'] = 'checkbox'

            # Select, NullBooleanSelect, SelectMultiple, RadioSelect, CheckboxSelectMultiple
            if widget_name in ['Select', 'NullBooleanSelect', 'SelectMultiple', 'RadioSelect', 'CheckboxSelectMultiple']:
                blueprint['choices'] = widget.choices

            # Yes-no radio select
            if widget_name == 'YesNoSwitch':
                blueprint['widget'] = 'yes_no_switch'

            # Select
            if widget_name == 'Select':
                blueprint['widget'] = 'select'
                if not blueprint['value']:
                    blueprint['value'] = None

            # NullBooleanSelect
            if widget_name == 'NullBooleanSelect':
                blueprint['widget'] = 'null_boolean_select'

            # SelectMultiple
            if widget_name == 'SelectMultiple':
                blueprint['widget'] = 'select_multiple'

            # RadioSelect
            if widget_name == 'RadioSelect':
                blueprint['widget'] = 'radio_select'
                if not blueprint['value']:
                    blueprint['value'] = u''

            # CheckboxSelectMultiple
            if widget_name == 'CheckboxSelectMultiple':
                blueprint['widget'] = 'checkbox_select_multiple'

            # MultiWidget
            if widget_name == 'MultiWidget':
                blueprint['widget'] = 'multi'

            # SplitDateTimeWidget
            if widget_name == 'SplitDateTimeWidget':
                blueprint['widget'] = 'split_datetime'

            # SplitHiddenDateTimeWidget
            if widget_name == 'SplitHiddenDateTimeWidget':
                blueprint['widget'] = 'split_hidden_datetime'

            # SelectDateWidget
            if widget_name == 'SelectDateWidget':
                blueprint['widget'] = 'select_date'
                blueprint['years'] = widget.years

            # Store field in either of collections
            if blueprint['hidden']:
                blueprint['attrs']['type'] = 'hidden'
                self.hidden.append(blueprint)
            else:
                self.fields[field] = blueprint

    def _get_widget(self, name, field):
        if name in self.meta_widgets:
            return self.meta_widgets[name]
        return field.widget


class FormFieldsets(object):
    """
    Hydrator that builds fieldset from form and blueprint
    """
    def __init__(self, form, fields, fieldsets=None):
        self.fieldsets = []

        # Use form layout
        if not fieldsets:
            try:
                fieldsets = form.layout
            except AttributeError:
                pass

        # Build fieldsets data
        if fieldsets:
            for blueprint in fieldsets:
                fieldset = {'legend': None, 'fields': [], 'help': None, 'last': False}
                fieldset['legend'] = blueprint[0]
                row_width = 0
                for field in blueprint[1]:
                    try:
                        if isinstance(field, basestring):
                            fieldset['fields'].append(fields[field])
                        elif field[0] == 'nested':
                            subfields = {'label': None, 'help_text': None, 'nested': [], 'errors':[], 'endrow': False, 'last': False, 'width': 100}
                            subfiels_ids = []
                            try:
                                subfields = field[2].update(subfields)
                            except IndexError:
                                pass
                            for subfield in field[1]:
                                if isinstance(subfield, basestring):
                                    subfiels_ids.append(subfield)
                                    subfields['nested'].append(fields[subfield])
                                    for error in fields[subfield]['errors']:
                                        if not error in subfields['errors']:
                                            subfields['errors'].append(error)
                                else:
                                    subfiels_ids.append(subfield[0])
                                    try:
                                        subfield[1]['attrs'] = dict(fields[subfield[0]]['attrs'], **subfield[1]['attrs'])
                                    except KeyError:
                                        pass
                                    subfields['nested'].append(dict(fields[subfield[0]], **subfield[1]))
                                    for error in fields[subfield[0]]['errors']:
                                        if not error in subfields['errors']:
                                            subfields['errors'].append(error)
                            if not subfields['label']:
                                subfields['label'] = subfields['nested'][0]['label']
                            if not subfields['help_text']:
                                subfields['help_text'] = subfields['nested'][0]['help_text']
                            try:
                                subfields['errors'] = form.errors["_".join(subfiels_ids)]
                            except KeyError:
                                pass
                            fieldset['fields'].append(subfields)
                        else:
                            try:
                                field[1]['attrs'] = dict(fields[field[0]]['attrs'], **field[1]['attrs'])
                            except KeyError:
                                pass
                            fieldset['fields'].append(dict(fields[field[0]], **field[1]))
                        row_width += fieldset['fields'][-1]['width']
                        if row_width >= 100:
                            fieldset['fields'][-1]['endrow'] = True
                            row_width = 0
                    except (AttributeError, IndexError, KeyError):
                        pass
                if fieldset['fields']:
                    fieldset['fields'][-1]['endrow'] = True
                    fieldset['fields'][-1]['last'] = True
                try:
                    fieldset['help'] = blueprint[2]
                except IndexError:
                    pass

                # Append complete fieldset
                if fieldset['fields']:
                    self.fieldsets.append(fieldset)
            self.fieldsets[-1]['last'] = True
