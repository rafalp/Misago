# Translation strings contextual markers style guide

Contextual markers clarify how a translation string is used. They help translators and prevent collisions when identical English strings (e.g., "Reply") require different translations in other languages.

Every translation string in Misago must include a contextual marker. The only exception is when using a translation string that already exists in Django itself, such as the 'This value is required.' validation message.


## Writing contextual markers

Misago uses the "feature" (or "view"/"form") followed by the "usage" convention for its contextual markers:

```python
class PrivateThreadMembersAddView:
    def post(...):
        # private thread members add (feature) + validation error (usage)
        if not permission:
            raise ValidationError(
                pgettext(
                    "private thread members add permission error",
                    "You don't have permission to do this!"
                )
            )

        if condition:
            raise ValidationError(
                pgettext(
                    "private thread members add validation error",
                    "You can't add more members!"
                )
            )

        messages.success(
            request,
            # private thread members add (feature) + success message (usage)
            pgettext("private thread members add success message", "Members added")
        )


# You don't have to be too specific in field labels and help strings
class UserRegisterForm:
    username = forms.CharField(
        label=pgettext_lazy("user register form", "Username"),
        help_text=pgettext_lazy(
            "user register form help text", "New user's name. Must be unique."
        ),
    )
```

This convention is also followed in templates:

```html
<title>
  {% translate "Make owner" context "private thread owner change page title" %}
</title>
<caption>
  {% translate "Make owner" context "private thread owner change confirm title" %}
</caption>
<p>
  {% translate "Change thread owner?" context "private thread owner change confirm prompt" %}
</p>
<button>
  {% translate "Make owner" context "private thread owner change confirm button" %}
</button>
<button>
  {% translate "Cancel" context "private thread owner change cancel button" %}
</button>
```