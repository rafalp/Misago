# Views, forms, templates and URLs style guide

Please note that this guide is not meant to be taken as gospel - justified exceptions are allowed. Practicality beats purity.


## Class-based views

Prefix the class name with the model or feature name when it makes sense:

```python
# Login page view for a "login" feature
class LoginView(View):
    ...


# Poll is a model and viewing poll votes is a feature...
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


# Private thread owner change is a feature
class PrivateThreadOwnerChangeView(View):
    pass


# Account is not a model, but it's a feature
class AccountPreferencesView(View):
    ...
```

Always suffix view class names with `View`:

```python
class SomeView(View):
    ...
```


## Forms

A form can be named after the view that uses it (or vice versa):

```python
# `LoginView`
class LoginForm(forms.Form):
    ...
```

The form’s name doesn’t have to match the view exactly:

```python
# `ThreadPollVoteView`
class PollVoteForm(forms.Form):
    ...
```


## Templates

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

For detail views, you can omit the `detail` part from the template name:

```python
class PrivateThreadDetailView(View):
    template_name = "private_thread/index.html"
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
    template_name = "thread_edit/index.html"
    template_name_htmx = "thread_edit/htmx.html"


class ThreadMoveView(View):
    template_name = "thread_move/index.html"
    template_name_modal = "thread_move/modal.html"
```

If a templates directory is shared by multiple features, you can use the suffix from the full template name:

```python
class PrivateThreadMembersAdd(View):
    template_name = "private_thread_members/add.html"
    template_name_htmx = "private_thread_members/add_modal.html"
```

If the full template includes the HTMX one, name the other template after the part of the page it represents:

```python
class ThreadEditView(View):
    template_name = "thread_edit/index.html"
    template_name_htmx = "thread_edit/form.html"
```

Sometimes there are many ways to organize templates. When this happens, use your best judgement.


## URLs

URL name should be based on the view class (or function) name, but drop the `View` suffix:

```python
path("/...", LoginView.as_view(), name="login")

path("/...", PollVotesView.as_view(), name="poll-votes")

path("/...", ThreadPollVotesView.as_view(), name="thread-poll-votes")

path("/...", ThreadStartView.as_view(), name="thread-start")

path("/...", PrivateThreadStartView.as_view(), name="private-thread-start")

path("/...", AccountPreferencesView.as_view(), name="account-preferences")
```

For a model’s default or detail view, you can use the model’s name instead:

```python
path("/...", ThreadDetailView.as_view(), name="thread")
```

Prefix the `id` url parameter with the model name:

```python
path("/t/<str:slug>/<int:thread_id>/", ThreadDetailView.as_view(), name="thread")
```