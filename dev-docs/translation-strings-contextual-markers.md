# Translation strings contextual markers style guide

Contextual markers clarify how a translation string is used. They help translators and prevent collisions when identical English strings (for example, “Reply”) require different translations in other languages.

Every translation string in Misago should include a contextual marker, except for translation strings that already exist in Django itself, such as the “This value is required.” validation message.


## Views

You can use the view name as a source of context for translation messages:

```python
class PrivateThreadMembersAddView:
    def get_context_data(...):
        return {
            "members_header": pgettext(
                "private thread add members header", "Add members"
            ),
        }

    def post(...):
        messages.success(
            request,
            pgettext("private thread members added", "Members added")
        )
```


## Forms and validators

For field labels and help texts, you can use the form name as the contextual marker:

```python
class UserRegisterForm:
    username = forms.CharField(
        label=pgettext_lazy("user register form", "Username"),
        help_text=pgettext_lazy(
            "user register form", "New user's name. Must be unique."
        ),
    )
```

You can use the same context for validation errors raised in forms, but for validators use a "noun validator" context instead:

```python
class UserRegisterForm:
    ...

    def clean_username(self):
        data = self.cleaned_data["username"]
        if not data:
            raise ValidationError(
                message=pgettext(
                    "user register form", "This user name is invalid."
                )
                code="invalid",
            )


def username_validator(data):
    if not data:
        raise ValidationError(
            message=pgettext(
                "username validator", "This user name is invalid."
            ),
            code="invalid",
        )
```

Permission checks use "nouns permission error" contexts for permission errors:

```python
def check_some_post_permission(user_permissions, post):
    if not user_permissions.is_moderator:
        raise PermissionDenied(
            pgettext(
                "posts permission error", "You can't do this."
            ),
        )
```


## Templates

There is no need to tie context markers in templates to views. Instead, context descriptions should match components or specific use cases.

`title` and `h1` elements likely are unique to the page:

```html
<title>
  {% translate "Make owner" context "private thread owner change page title" %}
</title>
<div class="page-header">
  <h1>{% translate "Make owner" context "private thread owner change page header" %}</h1>
</div>
```

For components, context can come from the component itself:

```html
{% translate "Post edit" context "post edit card header" %}

{% translate "Next page" context "post edits paginator" %}
```

For button labels, it’s good to emphasize their purpose in the context:

```html
<button>
  {% translate "Make owner" context "change owner submit btn" %}
</button>
<button>
  {% translate "Cancel" context "change owner cancel btn" %}
</button>
```