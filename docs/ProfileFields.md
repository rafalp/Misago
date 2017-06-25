Profile fields
==============

Misago allows your users to fill in additional details about themselves for other users to see on their profiles, such as their real name, gender, short bio or contact options such as homepage address or Twitter/Skype handles.

In addition to those, Misago also uses "read only" profile fields to displays users IP addresses on their profiles for forum moderators.


## Writing custom profile field

Under the hood, profile fields are Python classes inheriting from either the `misago.users.profilefields.ProfileField` class or one of higher-level base fields.

To write your own profile field, you'll need to create custom class that specifies following properties and methods:


### `fieldname`

The `fieldname` attribute specifies field's unique identifier in Misago. This identifier is used as key on `user.profile_fields` model field to store field's value as well as source form inputs `name` and `id` attributes.

Example "Website" field that specifies `website` as it's fieldname:

```python
class WebsiteField(basefields.UrlProfileField):
    fieldname = 'website'
    label = _("Website")
```


### `label` and `get_label`

Your field will have to define either `label` attribute, or `get_label(user)` method if you wish to customize the label content's depending on user's field contents.

Below field will always display "Skype ID" as its label:

```python
class SkypeHandleField(basefields.TextProfileField):
    fieldname = 'skype'
    label = _("Skype ID")
```

And example field that will look up user's gender before displaying label:

```python
class DynamicLabelField(basefields.TextProfileField):
    fieldname = 'dynamiclabelexample'
    
    def get_label(self, user):
        if user.profile_fields.get('gender') == 'female'
            return _("Your femine interest")
        if user.profile_fields.get('gender') == 'male':
            return _("Your masculine interest")
        return _("Your interest")
```


### `help_text` and `get_help_text`

If you wish to, your field may profile help text for display in forms that will provide additional help to users filling in their details.

Unlike label, the help text is displayed only in forms.

Below fields have no help text:

```python
class LocationField(basefields.TextProfileField):
    fieldname = 'location'
    label = _("Location")


class FullNameField(basefields.TextProfileField):
    fieldname = 'fullname'
    label = _("Full name")
    help_text = None
```

This field specifies help text via `help_text` property:

```python
class WebsiteField(basefields.UrlProfileField):
    fieldname = 'website'
    label = _("Website")
    help_text = _(
        "If you own page in the internet you wish to share on your profile "
        "you may enter its address here. Remember to for it to be valid http "
        "address starting with either http:// or https://"
    )
```

And this field builds help text using user's slug:

```python
class TwitterHandleField(basefields.TextProfileField):
    fieldname = 'twitter'
    label = _("Twitter handle")

    def get_help_text(self, user):
        return _(
            'If you own Twitter account, here you may enter your Twitter handle for other users '
            'to find you. Starting your handle with "@" sign is optional. Either "@%(slug)s" or '
            '"%(slug)s" are valid values.'
        ) % {
            'slug': user.slug
        }
```


### `readonly`

Defining `readonly = True` on field will make it never editable. This is useful when you are defining profile fields that display different information about user but are never editable on their own.

Example field that displays to moderators an IP address that user used to register account:

```python
class JoinIpField(basefields.TextProfileField):
    fieldname = 'join_ip'
    label = _("Join IP")
    readonly = True

    def get_value_display_data(self, request, user, value):
        if not request.user.acl_cache.get('can_see_users_ips'):
            return None

        return {
            'text': user.joined_from_ip
        }
```


### `is_editable`

The `is_editable` method allows you make field *conditionally* read-only.

Below profile field will be only editable by profile field's moderators:

```python
class ModeratorDescriptionField(basefields.UrlifiedTextareaProfileField):
    fieldname = 'moderatordescription'
    label = _("Moderator description")

    def is_editable(self, request, user):
        return request.user.acl_cache.get('can_moderate_profile_details')
```


### `get_form_field`

The `get_form_field` method is called to obtain form field that is then added to user edit form, plugging the field to Django's form handling mechanics.

This method is used in two places:

1. to add field to edit user form in admin control panel.
2. to add field to edit user details form used behind the courtain by Misago to clean and validate user details sent to API from "edit details" form in user options and on user profile pages.

This field uses `get_form_field` to specify `URLField` as field that should be used to edit its value:

```python
class WebsiteField(basefields.UrlProfileField):
    fieldname = 'website'
    label = _("Website")

    def get_form_field(self, request, user):
        return forms.URLField(
            label=self.get_label(user),
            help_text=self.get_help_text(user),
            initial=user.profile_fields.get(self.fieldname),
            max_length=250,
            disabled=self.readonly,
            required=False,
        )
```

Notice that the fact that this field is hidden from users outside of admin control panel means that you may use it to specify admin-oriented `label` and `help_text` within it, and use `label` and `help_text` props documented ealier for user-facing UI.

Also take a note that while its not necessary, its good practice for all profile fields to be optional, and thus specify `required=False` on field returned by `get_form_field`.


### `get_form_field_json`

This method is called to obtain the JSON describing how to build edit field in JavaScript UI. Because default implementation provided by the `ProfileField` is versalite enough for great majority of use cases, its unlikely that you'll ever want to write custom implementation for your fields, instead limiting yourself to editing the `get_input_json` exclusively.

```python
class FullNameField(basefields.TextProfileField):
    fieldname = 'fullname'
    label = _("Full name")

    def get_form_field_json(self, request, user):
        # default implementation inherited from ProfileField
        return {
            'fieldname': self.fieldname,
            'label': self.get_label(user),
            'help_text': self.get_help_text(user),
            'initial': user.profile_fields.get(self.fieldname, ''),
            'input': self.get_input_json(request, user),
        }
```

Very much alike the `get_form_field` documented ealier, because this method is origin of truth for details edit forms in user-facing UI, you may modify it to customize field's label and help text.


### `get_input_json`

This method is called to obtain the JSON describing field input to create in end-user facing forms.

It supports either of those inputs:

```python
# this field will use text input
class FullNameField(basefields.TextProfileField):
    fieldname = 'fullname'
    label = _("Full name")

    def get_input_json(self, request, user):
        return {
            'type': 'text',
        }


# this field will use textarea
class BioField(basefields.UrlifiedTextareaProfileField):
    fieldname = 'bio'
    label = _("Bio")

    def get_input_json(self, request, user):
        return {
            'type': 'textarea',
        }


# this field will use select input
class GenderField(basefields.ChoiceProfileField):

    # ...

    def get_input_json(self, request, user):
        choices = []
        for key, choice in self.get_choices():
            choices.append({
                'value': key,
                'label': choice,
            })

        return {
            'type': 'select',
            'choices': [
                {
                    'value': '',
                    'label': _("Not specified"),
                },
                {
                    'value': 'female',
                    'label': _("Female"),
                },
                {
                    'value': 'male',
                    'label': _("Male"),
                },
            ],
        }
```

Misago comes with convenience base classes for popular input types like text, textarea or select, that are documented further into this document.


### `clean`

In addition to cleaning and validation logic implemented by the form field returned in `get_form_field`, you may include custom cleaning and validation logic on your field that gets run as part of form's clean and validate process.

Below example shows field that performs additional validation and cleanup on user-entered twitter handle:

```python
class TwitterHandleField(basefields.TextProfileField):
    fieldname = 'twitter'
    label = _("Twitter handle")

    def clean(self, request, user, data):
        data = data.lstrip('@')
        if data and not re.search('^[A-Za-z0-9_]+$', data):
            raise ValidationError(ugettext("This is not a valid twitter handle."))
        return data
```

Field's `clean` method is called only when user filled it in edit form. It should return cleaned value, or raise ValidationError on any errors. Those errors will be associated with and displayed by their fields in form.


### `get_display_data`

Just like the `get_input_json` returns JSON describing how form field should be displayed in user-facing edit interface, the `get_display_data` should return JSON describing how its value should be displayed on user's "details" tab in profile. This field is also well covered by the default implementation provided by the `ProfileField` class, which does following:

1. If user's profile doesn't have value for field that we are trying to display, and field is not always readonly, return `None`, telling interface to don't display it.
2. Call the `get_value_display_data` method to obtain JSON describing how field's value should be displayed on the page. If this method returns `None`, don't display field on user's profile.
3. Add field's name and label to returned JSON.

```python
class ProfileField(object):
    
    # ...

    def get_display_data(self, request, user):
        value = user.profile_fields.get(self.fieldname, '')
        if not self.readonly and not len(value):
            return None

        data = self.get_value_display_data(request, user, value)
        if not data:
            return None

        data.update({
            'fieldname': self.fieldname,
            'name': text_type(self.get_label(user)),
        })

        return data
```

Because of such generic implementation, you'll likely limit yourself to customizing the `get_value_display_data` when writing your fields, and only ever use this method if you want to customize displayed label.


### `get_value_display_data`

This method returns JSON describing how field's value should be displayed on user's profile page. Misago supports quite a few display methods for profile fields:

```python
# Display value in paragraph
class FullNameField(basefields.TextProfileField):
    
    # ...

    def get_value_display_data(self, request, user, value):
        return {
            'type': 'text',
        }


# Display value as html
class BioField(basefields.TextareaProfileField):
    
    # ...
    
    def get_value_display_data(self, request, user, value):
        return {
            'html': html.linebreaks(html.escape(value)),
        }


# Display value as link
class WebsiteField(basefields.UrlProfileField):
    
    # ...
    
    def get_value_display_data(self, request, user, value):
        return {
            'url': value,
        }


# Display value as link with text label
class TwitterHandleField(basefields.UrlProfileField):
    
    # ...
    
    def get_value_display_data(self, request, user, value):
        return {
            'text': '@{}'.format(data),
            'url': 'https://twitter.com/{}'.format(data),
        }
```

In default implementation provided by the `ProfileField`, this field is called by the `get_display_data`. As such its prefferable in most cases for field to provide custom `get_value_display_data` instead of `get_display_data`.

As documented in the `get_display_data`, returning `None` from this methid will prevent this field from beind displayed on user's profile.


### `search_users`

This method is called by search function available on users lists in admin control panel, to search users that have profile field with specified value. Its called with single argument, `criteria`, that contains search string entered in search form, and should return `None` or `Q` object that lets Misago search field's value.

The `ProfileField` class implements generic `search_users` implementation that assumes that field's value is text and performs *case sensitive* search on users `profile_fields` value as well as excludes readonly fields from search:

```python
class ProfileField(object):

    # ...

    def search_users(self, criteria):
        if self.readonly:
            return None

        return Q(**{
            'profile_fields__{}__contains'.format(self.fieldname): criteria
        })
```

In addition to this `ChoiceProfileField` base field provides custom implementation that searches users by label and value of their choice.


## Base fields

## Default fields

## Obtaining list of profile fields keys existing in database

## Removing profile fields from database

## Using logging for controling profile fields usage