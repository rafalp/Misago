Database Settings
=================

Those settings are stored in database and are available via `misago.conf.settings`. To change those settings you need to use admin control panel.


## account_activation

Preffered way in which new user accounts are activated. Can be either of those:

* `none` - no activation required.
* `user` - new user has to click link in activation e-mail.
* `admin` - board administrator has to activate new accounts manually.
* `block` - turn new registrations off.


## allow_custom_avatars

Controls if users may set avatars from outside forums.


## avatar_upload_limit

Max allowed size of uploaded avatars in kilobytes.


## default_avatar

Default avatar assigned to new accounts. Can be either `initials` for randomly generated pic with initials, `gravatar` or `gallery` which will make Misago pick random avatar from gallery instead.


## default_timezone

Default timezone used by guests and newly registered users that haven't changed their timezone prefferences.


## forum_branding_display

Controls branding's visibility in forum navbar.


## forum_branding_text

Allows you to include text besides brand logo on your forum.


## forum_name

Forum name, displayed in titles of pages.


## forum_index_meta_description

Forum index Meta Description used as value meta description attribute on forum index.


## forum_index_title

Forum index title. Can be empty string if not set, in which case `forum_name` should be used instead.


## post_length_max

Maximal allowed post content length.


## post_length_min

Minimal allowed post content length.


## signature_length_max

Maximal allowed length of users signatures.


## subscribe_reply

Default value for automatic subscription to replied threads prefference for new user accounts. Its value represents one of those settings:

* `no` - don't watch.
* `watch` - put on watched threads list.
* `watch_email` - put on watched threads list and send e-mail when somebody replies.


## subscribe_start

Default value for automatic subscription to started threads prefference for new user accounts. Allows for same values as `subscribe_reply`.


## thread_title_length_max

Maximal allowed thread title length.


## thread_title_length_min

Minimal allowed thread title length.


## username_length_max

Maximal allowed username length.


## username_length_min

Minimal allowed username length.

