# Naming conventions

This document is a guide to naming conventions used in the codebase. Please don't treat it as gospel - not everything has a naming convention, and justified exceptions are allowed.


## Class-based views, forms, templates and url names

### Views

Prefix the class name with the model or feature name when it makes sense:

```python
# Login page view
class LoginView(View):
    ...


# Poll a model and viewing poll votes is a feature...
class PollVotesView(View):
    ...


# ...but if a poll is only accessed through another model or feature, we use a compound name
class ThreadPollVotesView(View):
    ...


# Thread start is a feature
class ThreadStartView(View):
    pass


# Private thread start is a feature
class PrivateThreadStartView(View):
    pass


# Account is not a model, but "forum account" is a feature
class AccountPreferencesView(View):
    ...
```

Always suffix view class names with `View`:

```python
class SomeView(View):
    ...
```


### Forms

If the view uses a single form, name it after the view, but change the suffix to `Form`:

```python
# `LoginView`
class LoginForm(forms.Form):
    ...


# `PrivateThreadAddMembersView`
class PrivateThreadAddMembersForm(forms.Form):
    ...
```


### Templates

Template name should based on the view class (or function) name, but drop the `view` suffix:

```python
class LoginView(View):
    template_name = "login.html"


class PollVotesView(View):
    template_name = "poll_votes.html"


class ThreadPollVotesView(View):
    template_name = "thread_poll_votes.html"


class PrivateThreadStartView(View):
    template_name = "private_thread_start.html"
```

To make a view's templates easier to customize, break them into smaller parts and keep them in directories named after the view:

```python
class PrivateThreadStartView(View):
    template_name = "private_thread_start/index.html"
```

If multiple views are closely related (e.g., each view handles a different tab or a section of a single page), you can put their templates in the same directory:

```python
class AccountPreferencesView(View):
    template_name = "account/preferences.html"


class AccountChangePassworsView(View):
    template_name = "account/change_password.html"
```

If a view or component has both a regular and an HTMX version, you can differentiate the template name based on its use. E.g.:

```python
class ThreadEditView(View):
    template_name = "thread_edit/full.html"
    template_name_htmx = "thread_edit/htmx.html"


class ThreadMoveView(View):
    template_name = "thread_move/full.html"
    template_name_modal = "thread_move/modal.html"


class PrivateThreadAddMembers(View):
    template_name = "private_thread_members/add_full.html"
    template_name_htmx = "private_thread_members/add_htmx.html"
```

Sometimes the full template includes the HTMX one. In this case, name the other template after the part of the page it contains:

```python
class ThreadEditView(View):
    template_name = "thread_edit/full.html"
    template_name_htmx = "thread_edit/form.html"
```

Sometimes there are many ways to organize templates. When this happens, use your best judgement.


### Urls

URL name should be based on the view class (or function) name, but drop the `View` suffix:

```python
path("/...", LoginView.as_view(), name="login")

path("/...", PollVotesView.as_view(), name="poll-votes")

path("/...", ThreadPollVotesView.as_view(), name="thread-poll-votes")

path("/...", ThreadStartView.as_view(), name="thread-start")

path("/...", PrivateThreadStartView.as_view(), name="private-thread-start")

path("/...", AccountPreferencesView.as_view(), name="account-preferences")
```
