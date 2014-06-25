=========================
Writing New Admin Actions
=========================


Misago Admin vs. Django Admin
=============================

Misago brings its own admin site just like Django `does <https://docs.djangoproject.com/en/1.6/#the-admin>`_. This means you have to make a decision which one your app will use for administration.

If you intend to be sole user of your app, Django admin will propably be faster to get going. However if you plan for your app to be available to wider audience, its good for your admin interface to be part of Misago admin site. This will require you to write more code than in case you've went Django way, but will give your users more consistent experience and, in case for some languages, save them of quirkyness that comes with Django admin automatically created messages.


Creating Admin Views
===================


Writing views
-------------

Unlike Django, Misago admin is not "automagical". This means you will not get complete admin from nowhere by just creating one file and writing 3 lines of code in it. However Misago provides set of basic classes defined in  in :py:mod:`misago.admin.views.generic` module that can offload most of burden of writing views handling items lists and forms from you.

Workflow with those classes is fast and easy to master. First, you define your own mixin (propably extending ``AdminBaseMixin``). This mixin will define common properties and behaviour of all admin views, like which Model are admin views focused on, how to fetch its instances from database as well as where to seek templates and which message should be used when model could not be found.

Next you define your own views inheriting from your mixin and base views. Misago provides basic views for each of most common scenarios in admin:

* **ListView** - For items lists. Supports pagination, sorting, filtering and mass actions.
* **FormView** and **ModelFormView** - For displaying and handling forms submissions.
* **ButtonView** - For handling state-changing button presses like "delete item" actions.


AdminBaseMixin
--------------

:py:class:`misago.admin.views.generic.AdminBaseMixin`


Base class for admin mixins that contain properties and behaviours shared between admin views. While you are allowed to set any properties and function on your own mixins to dry your admin views more, bare minimum expected from you is following:

* **Model** property or **get_model(self)** function used to get model type.
* **root_link** property that is string with link name for "index" view for admin actions (usually link to items list).
* **templates_dir** property being string with name of directory with admin templates used by mixin views.

Optionally if you don't plan to set up action-specific item not found messages, you may set ``message_404`` property on mixin to make all your views use same message when requested model could not be found.


ListView
--------

:py:class:`misago.admin.views.generic.ListView`

Base class for lists if items. Supports following properties:

* **template** - name of template file located in ``templates_dir`` used to render this view. Defaults to ``list.html``
* **items_per_page** - integer controlling number of items displayed on single page. Defaults to 0 which means no pagination
* **SearchForm** - Form type used to construct form for filtering this list. Either this field or ``get_search_form`` method is required to make list searchable.
* **ordering** - list of supported sorting methods. List of tuples. Each tuple should countain two items: name of ordering method (eg. "Usernames, descending") and ``order_by`` argument ("-username"). Defaults to none which means queryset will not be ordered. If contains only one element, queryset is ordered, but option for changing ordering method is not displayed.

In addition to this, ListView defines following methods that you may be interested in overloading:


.. function:: get_queryset(self)

This function is expected to return queryset of items that will be displayed. If filters, sorting or pagination is defined, this queryset will be sliced and filtered.


.. function:: add_item_action(cls, name, icon, link, style=None)

Class method that allows you to add custom links to item actions. Link should be a string with link name, not complete link. It should also accept same kwargs as other item actions links.


.. function:: get_search_form(self, request):

This function is used to get search form class that will be used to construct form for searching list items.

If you decide to make your list searchable, remember that your Form must meet following requirements:

* Must define ``filter_queryset(self, search_criteria, queryset)`` method that will be passed unfiltered queryset, which it should modify using filter/exclude clauses and data from search_criteria.
* Must return queryset.
* Must not define fields that use models for values.


FormView
--------

:py:class:`misago.admin.views.generic.FormView`

Base class for forms views.

* **template** - name of template file located in ``templates_dir`` used to render this view. Defaults to ``form.html``
* **Form** property or **create_form_type** method - ``create_form`` method is called with ``request`` as its argument and is expected to return form type that will be used by view. If you need to build form type dynamically, instead of defining ``Form`` property, define your own ``create_form``.


.. function:: create_form_type(self, request)

Returns form type that will be used to create form instance. By default returns value of ``Form`` property.


.. function:: initialize_form(self, FormType, request)

Initializes either bound or unbound form using request and ``FormType`` provided.


.. function:: handle_form(self, form, request)

If form validated successfully, this method is called to perform action. Here you should place code that will read data from form, perform actions on models and set result message. Optionally you may return ``HttpResponse`` from this function. If nothing is returned, view returns redirect to ``root_link``.

Optionally your form template may have button with ``name="stay"`` attribute defined, pressing which will cause view to redirect you to clean form instead.


ModelFormView
-------------

:py:class:`misago.admin.views.generic.ModelFormView`

Base class for targetted forms views. Its API is largery identic to ``FormView``, except it's tailored at handling ``ModelForm`` and modifying model states. All methos documented for ``FormView`` are present in ``ModelformView``, but they accept one more argument named "target", containing model instance to which model form will be tied.

In addition, this view comes with basic definition for form handler that calls ``save()`` on model instance and (if defined) sets success message using value of objects ``message_submit`` parameter.


ButtonView
----------

:py:class:`misago.admin.views.generic.ButtonView`

Base class for handling non-form based POST requests.

Do control this view behaviour, define your own ``button_action`` method:


.. function:: button_action(self, request, target)

This function is expected to perform requested action on target provided and set result message on ``request``.

It may return nothing or ``HttpResponse``. If nothing is returned, view returns redirect to ``root_link`` instead.


Targeted views
--------------

Both ``ModelFormView`` and ``ButtonView`` are called "targeted views", because they are expected to manipulate model instances. They both inherit from ``TargetedView`` view, implements simple API that is used for associating request with corresponding model instance:


.. function:: get_target_or_none(self, request, kwargs)

Function expected return valid model instance or None. If None is returned, this makes view set error message using ``message_404`` attribute and returns redirect to ``root_link``.


.. function:: get_target(self, kwargs)

Called by ``get_target_or_none``.

If ``kwargs`` len is 1, its assumed to be value of seeked model pk value. This makes function call model manager ``get()`` method to fetch model instance from database. Otherwhise "empty" instance is created and returned instead. Eventual ``DoesNotExist`` errors are handled by ``get_target_or_none``.


.. function:: check_permissions(self, request, target)

Once model instance is obtained either from database or empty instance is created, this function is called to see intended action is allowed for this request and target. This function is expected to return ``None`` if no issues are found or string containing error message. If string is returned, its set as error messages, and view interrupts its execution by returning redirect to ``root_link``.


.. note::
   While target argument value is always present, you don't have to do anything with it if its not making any sense for your view.


Adding extra values to context
------------------------------

Each view calls its ``process_context`` method before rendering template to response. This method accepts two arguments:

* **request** - HttpRequest instance received by view.
* **context** - Dict that is going to be used to render template.

It's required to return dict that will be then used as one of arguments to call ``render()``.


Registering in Misago Admin
===========================

Misago Admin Site is just an hierarchy of pages, made of two parts: ``site`` that contains tree of links and ``urlpatterns`` that is included in ``misago:admin`` namespace.

When Misago is started, it scans registered apps for ``admin`` module, just like Django admin does. If module is found, Misago checks if it defines ``MisagoAdminExtension`` class. If such class is found, its instantiated with no arguments, and two of its methods are called:


.. function:: register_urlpatterns(self, urlpatterns)

This function allows apps to register new urlpatterns under ``misago:admin`` namespace.


.. function:: register_navigation_nodes(self, site)

This function allows apps to register new links in admin site navigation.


Registering urls under ``misago:admin`` namespace
-------------------------------------------------

Admin links are stored within instance of special object :py:class:`misago.admin.urlpatterns.URLPatterns` available as ``urlpatterns`` argument passed to ``register_urlpatterns`` method. This object exposes two methods as public api:


.. function:: namespace(path, namespace, parent=None)

Registers new namespace in admin links hierarchy.

* **path** - Path prefix for links within this namespace. For example ``r'^users/'``.
* **namespace** - Non-prefixed (eg. without ``misago:admin`` part) namespace name.
* **parent** - Optional. Name of parent namespace (eg. ``users:accounts``).


.. function:: patterns(namespace, *urlpatterns)

Registers urlpatterns under defined namespace. Expects first argument to be name of namespace that defined links belong to (eg. ``users:accounts``). Every next argument is expected to be valid Django link created with ``url`` function from :py:mod:`django.conf.urls` module.


.. note::
   ''misago:admin'' prefix of namespaces is implicit. Do not prefix namespaces passed as arguments to those functions with it.


Registering urls in navigation
------------------------------

Your urls have to be discoverable by your users. Easiest way is to do this is to display primary link to your admin action in admin site navigation.

This navigation is controlled by instance of the :py:class:`misago.admin.hierarchy.AdminHierarchyBuilder` class available as ``site`` argument passed to ``register_navigation_nodes`` method of your ``MisagoAdminExtension`` class. It has plenty of functions, but it's public api consists of one method:


.. function:: add_node(name=None, icon=None, parent='misago:admin', after=None, before=None, namespace=None, link=None)


This method accepts following named arguments:

* **parent** - Name of parent namespace under which this action link is displayed.
* **after** - Link before which one this one should be displayed.
* **before** - Link after which one this one should be displayed.
* **namespace** - This link namespace.
* **link** - Link name.
* **name** - Link title.
* **icon** - Link icon (both `Glyphicons <http://getbootstrap.com/components/#glyphicons>`_ and `Font Awesome <http://fontawesome.io/icons/>`_ are supported).

Only last three arguments are required. ``after`` and ``before`` arguments are exclusive. If you specify both, this will result in an error.

Misago Admin supports three levels of hierarchy. Each level should corelate to new namespace nested under ``misago:admin``. Depending on complexity of your app's admin, it can define links that are one level deep, or three levels deep.


Adding actions to items lists
-----------------------------

Other way to make your views reachable is to include links to them on items lists. To do this, you may use ``add_item_action`` classmethod of ListView class that is documented above.
