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


### `get_form_field`
### `get_form_field_json`
### `get_input_json`
### `clean`
### `get_display_data`
### `get_value_display_data`
### `search_users`


## Read only profile fields

## Base fields

## Default fields

## Obtaining list of profile fields keys existing in database

## Removing profile fields from database

## Using logging for controling profile fields usage