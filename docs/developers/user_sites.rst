====================
Extending User Sites
====================

There are three sites associated with user accounts:

* User Control Panel
* User Profiles List
* User Profile

Each of those sites consists of its own layout and list of pages. For example, User Profile layout displays user name, information about user status, and pages (tabs) with lists of user threads, posts, followers and likes.

Each site is associated to instance of special object, :py:class:`misago.users.sites.Site`, which contains list of all pages belonging to it. Those instances are :py:object:`misago.users.sites.usercp`, :py:object:`misago.users.sites.users_list` and :py:object:`misago.users.sites.user_profile`.

:py:class:`misago.users.sites.Site` instances expose following API:


.. function:: add_page(link, name, icon=None, after=None, before=None,
                 	   visibility_condition=None)

Adds page to site. ``after`` and ``before`` arguments should be value of other page ``link``. ``visibility_condition`` argument accepts callable that will be called with args passed to ``get_pages`` function on page render to resolve if link to page should be displayed.


.. function:: get_pages(link, request, profile=None)

Returns list of pages assigned to this site. Each page is a dict of kwargs passed to ``add_page`` with additional ``is_active`` argument that controls if selected page is displayed one.


.. function:: get_default_link()

Returns default link name that should be used as argument for ``{% url %}`` template tag.

Default links for Misago sites are available in templates trough following variables:

* **USERCP_URL** - Default link to user control panel site.
* **USERS_LIST_URL** - Default link to users lists site.
* **USER_PROFILE_URL** - Default link to user profile site.


Adding pages to User Control Panel
==================================

To add custom page to UserCP, register it on :py:object:`misago.users.sites.usercp` object using ``add_page`` method described above.

After this, write your view(s), making sure they are using :py:object:`misago.users.views.usercp.render` function instead of :py:object:`django.shortcuts.render` to render response, and that your templates are extending ``misago/usercp/base.html`` template, defining custom html in ``page`` block instead of usual ``content``.
