Shortcut functions
==================

Just like [Django](https://docs.djangoproject.com/en/{{ book.django_version }}/topics/http/shortcuts/), Misago defines shortcuts module that reduce some procedures to single functions.

This module lives in `misago.views.shortcuts` and in addition to Misago-native shortcut functions, it imports whole of `django.shortcuts`, so you don't have to import it separately in your views.


## `paginate(object_list, page, per_page, orphans=0, allow_empty_first_page=True)`

This function is a factory that validates received data and returns [Django's Page](https://docs.djangoproject.com/en/{{ book.django_version }}/topics/pagination/#page-objects) object. In adition it also translates `EmptyPage` errors into `Http404` errors and validates if first page number was explictly defined in url parameter or not.

`paginate` function has certain requirements on handling views that use it. Firstly, views with pagination should have two links instead of one:

```python
# inside blog.urls.py
urlpatterns += patterns('blog.views',
    url(r'^/$', 'index', name='index'),
    url(r'^/(?P<page>[1-9][0-9]*)/$', 'index', name='index'),
)

# inside blog.views.py
def index(request, page=None):
    # your view that calls paginate()
```


##### Note

Giving `page` argument default value of 1 will make `paginate` function assume that first page was reached via link with explicit first page number and cause redirect loop.

Error handler expects link parameter that contains current page number to be named "page". Otherwise it will fail to create new link and raise `KeyError`.


## `validate_slug(model, slug)`

This function compares model instance's "slug" attribute against user-friendly slug that was passed as link parameter. If model's slug attribute is different this function, `misago.views.OutdatedSlug` is raised. This exception is then captured by Misago's exception handler which makes Misago return permanent (http 301) redirect to client with valid link.

Example of view that first fetches object form database and then makes sure user or spider that reaches page has been let known of up-to-date link:

```python
from misago.views.shortcuts import validate_slug, get_object_or_404
from myapp.models import Cake

def cake_fans(request, cake_id, cake_slug):
    # first get cake model from DB
    cake = get_object_or_404(Cake, pk=cake_id)
    # issue redirect if cake slug is invalid
    validate_slug(cake, cacke_slug)
```


##### Notes

You may have noticed that there's no exception handling for either `Http404` exception raised by `get_object_or_404`, nor `OutdatedSlug` exception raised by `validate_slug`. This is by design. Both exceptions are handled by Misago for you so you don't have to spend time writing exception handling boiler plate on every view that fetches objects from database and validates their links.

Naturally if you need to, you can still handle them yourself.

Also, your links should use "slug" parameters only when they are supporting GET requests. For same reason you should call `validate_slug` only when request method is GET or HEAD.