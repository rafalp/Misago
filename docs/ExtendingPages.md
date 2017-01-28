Adding sections to existing pages
=================================

Certain pages in Misago are simple containers for sections:

* User Control Panel
* User Profiles List
* User Profile

Each of those consists of its own layout and list of sections. For example, user profiles display user name, information about user status, and sections (tabs) with lists of user threads, posts, followers, name history, etc. ect..

Each section is associated to instance of special object, `misago.core.page.Page`, which contains list of all sections belonging to it. Those instances are `misago.users.sites.usercp`, `misago.users.sites.users_list` and `misago.users.sites.user_profile`.

`misago.core.page.Page` instances expose following API:


### `add_section(link, after=None, before=None, visible_if=None, get_metadata=None, **kwargs)`

Adds section to page. `after` and `before` arguments should be value of other page `link`. `visible_if` argument accepts callable that will be called with args passed to `get_pages` function on page render to resolve if link to page should be displayed. `get_metadata` can be callable returning additional computed metadata for this page. All other values passed to function call get preserved in order to make it easy for 3rd party developers to reuse mechanic for their apps.

`visible_if` and `get_metadata` functions are called with arguments that were passed to `get_sections` method.


### `get_sections(request, *args)`

Returns list of sections assigned to this page. Each section is a dict of kwargs passed to `add_section` with additional `is_active` argument that controls if selected page is displayed one and `metadata` dict if one is defined.


### `get_default_link()`

Returns default link name that should be used as argument for `{% url %}` template tag.

Default links for Misago user pages are available in templates through following variables:

* `USERCP_URL` - Default link to user control panel site.
* `USERS_LIST_URL` - Default link to users lists site.
* `USER_PROFILE_URL` - Default link to user profile site.