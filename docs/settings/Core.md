Core Settings
=============

Those settings are set in `settings.py` file with defaults defined in `misago.conf.defaults` module. 


## `MISAGO_403_IMAGE`

Url (relative to `STATIC_URL`) to file that should be served if user has no permission to see requested attachment.


## `MISAGO_404_IMAGE`

Url (relative to `STATIC_URL`) to file that should be served if user has requested nonexistant attachment.


## `MISAGO_ACL_EXTENSIONS`

List of Misago ACL framework extensions.


## `MISAGO_ADMIN_NAMESPACES`

Link namespaces that are administrator-only areas that require additional security from Misago. Users will have to re-authenticate themselves to access those namespaces, even if they are already signed in your frontend. In addition they will be requested to reauthenticated if they were inactive in those namespaces for certain time.

Defautly `misago:admin` and `admin` namespaces are specified, putting both Misago and Django default admin interfaces under extended security mechanics.


## `MISAGO_ADMIN_PATH`

Path prefix for Misago administration backend. Defautly "admincp", but you may set it to empty string if you with to disable your forum administration backend.


## `MISAGO_ADMIN_SESSION_EXPIRATION`

Maximum allowed lenght of inactivity period between two requests to admin namespaces. If its exceeded, user will be asked to sign in again to admin backed before being allowed to continue activities.


## `MISAGO_ATTACHMENT_IMAGE_SIZE_LIMIT`

Max dimensions (width and height) of user-uploaded images embedded in posts. If uploaded image is greater than dimensions specified in this settings, Misago will generate thumbnail for it.


##### Note

Because user-uploaded GIF's may be smaller than dimensions specified, but still be considerably heavy due to animation, Misago always generates thumbnails for user-uploaded GIFS, stripping the animations from them.


## `MISAGO_ATTACHMENT_ORPHANED_EXPIRE`

How old (in minutes) should attachments unassociated with any be before they'll automatically deleted by `clearattachments` task.


## `MISAGO_ATTACHMENT_SECRET_LENGTH`

Length of attachment's secret (filenames and url token). The longer, the harder it is to bruteforce, but too long may conflict with your uploaded files storage limits (eg. filesystem path length limits).


##### Warning

In order for Misago to support clustered deployments or CDN's (like Amazon's S3), its unable to validate user's permission to see the attachment at its source. Instead it has to rely on exessively long and hard to guess urls to attachments and assumption that your users will not "leak" source urls to attachments further.

Generaly, neither you nor your users should use forums to exchange files containing valuable data, but if you do, you should make sure to secure it additionaly via other means like password-protected archives or file encryption solutions.


## `MISAGO_AVATAR_GALLERY`

Path to directory containing avatar galleries. Those galleries can be loaded by running `loadavatargallery` command.

Feel free to remove existing galleries or add your own.

If you create gallery named `__default__` and set avatar gallery as default user avatar, Misago will select new users avatars from it while keeping this gallery hidden from existing users.


## `MISAGO_AVATARS_SIZES`

Misago uses avatar cache that prescales avatars to requested sizes. Enter here sizes to which those should be optimized.


##### Warning

It's impossible to regenerate user avatars store for existing avatars. Misago comes with sane defaults for avatar sizes, with min. height for user avatar being 400 pixels square, and steps of 200, 150, 100, 64, 50 and 30px. However if you need larger avatar or different pregenerated dimensions, changing those will require you to manually remove `avatars` directory from your media storage as well as running `misago.users.avatars.set_default_avatar` function against every user registered.


## `MISAGO_BLANK_AVATAR`

This path to image file that Misago should use as blank avatar.


## `MISAGO_COMPACT_DATE_FORMAT_DAY_MONTH`

Date format used by Misago `compact_date` filter for dates in this year.

Expects standard Django date format, documented [here](https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date)


## `MISAGO_COMPACT_DATE_FORMAT_DAY_MONTH_YEAR`

Date format used by Misago `compact_date` filter for dates in past years.

Expects standard Django date format, documented [here](https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date)


## `MISAGO_DIALY_POST_LIMIT`

Dialy limit of posts that may be posted from single account. Fail-safe for situations when forum is flooded by spam bot. Change to 0 to lift this restriction.


## `MISAGO_DYNAMIC_AVATAR_DRAWER`

Function used to create unique avatar for this user. Allows for customization of algorithm used to generate those.


## `MISAGO_EVENTS_PER_PAGE`

Misago reads events to display in separate database query to avoid situation when thread with large number of eg. moderator actions displays pages consisting exclusively of events. Using this setting you may specify upper limit of events displayed on thread's single page. This setting is intented as fail safe, both to save threads from excessively long lists of events your users will have to scroll trough, as well as to keep memory usage within limts.

In case of more events than specified being found, oldest events will be truncated.


## `MISAGO_HOURLY_POST_LIMIT`

Hourly limit of posts that may be posted from single account. Fail-safe for situations when forum is flooded by spam bot. Change to 0 to lift this restriction.


## `MISAGO_LOGIN_API_URL`
URL to API endpoint used to authenticate sign-in credentials. Musn't contain api prefix or wrapping slashes. Defaults to 'auth/login'.


## `MISAGO_MARKUP_EXTENSIONS`

List of python modules extending Misago markup.


## `MISAGO_MOMENT_JS_LOCALES`

List of Moment.js locals available.


## `MISAGO_NEW_REGISTRATIONS_VALIDATORS`

List of functions to be called when somebody attempts to register on forums using registration form.


## `MISAGO_NOTIFICATIONS_MAX_AGE`

Max age, in days, of notifications stored in database. Notifications older than this will be delted.


## `MISAGO_POST_ATTACHMENTS_LIMIT`

Limit of attachments that may be uploaded in single post. Lower limits may hamper image-heavy forums, but help keep memory usage by posting process. 


## `MISAGO_POST_SEARCH_FILTERS`

List of post search filters that are used to normalize search queries and documents used in forum search engine.


## `MISAGO_POST_VALIDATORS`

List of post validators used to validate posts.


## `MISAGO_POSTING_MIDDLEWARES`

List of middleware classes participating in posting process.


## `MISAGO_POSTS_PER_PAGE`

Controls number of posts displayed on thread page. Greater numbers can increase number of objects loaded into memory and thus depending on features enabled greatly increase memory usage.


## `MISAGO_POSTS_TAIL`

Defines minimal number of posts for thread's last page. If number of posts on last page is smaller or equal to one specified in this setting, last page will be appended to previous page instead.


## `MISAGO_RANKING_LENGTH`

Some lists act as rankings, displaying users in order of certain scoring criteria, like number of posts or likes received.
This setting controls maximum age in days of items that should count to ranking.


## `MISAGO_RANKING_SIZE`

Maximum number of items on ranking page.


## `MISAGO_READTRACKER_CUTOFF`

Controls amount of data used by readtracking system. All content older than number of days specified in this setting is considered old and read, even if opposite is true. Active forums can try lowering this value while less active ones may wish to increase it instead.


## `MISAGO_SEARCH_CONFIG`

PostgreSQL text search configuration to use in searches. Defaults to "simple", for list of installed configurations run "\dF" in "psql".

Standard configs as of PostgreSQL 9.5 are: `dutch`, `english`, `finnish`, `french`, `german`, `hungarian`, `italian`, `norwegian`, `portuguese`, `romanian`, `russian`, `simple`, `spanish`, `swedish`, `turkish`.

Example on adding custom language can be found [here](https://github.com/lemonskyjwt/plpstgrssearch).


##### Note

Items in Misago are usually indexed in search engine on save or update. If you change search configuration, you'll need to rebuild search for past posts to get reindexed using new configuration. Misago comes with `rebuildpostssearch` tool for this purpose.


## `MISAGO_SLUGIFY`

Path to function or callable used by Misago to generate slugs. Defaults to `misago.core.slugify.default`. Use this function if you want to customize slugs generation on your community.


## `MISAGO_STOP_FORUM_SPAM_MIN_CONFIDENCE`

Minimum confidence returned by [Stop Forum Spam](http://www.stopforumspam.com/) for Misago to reject new registration and block IP address for 1 day.


## `MISAGO_THREADS_ON_INDEX`

Change this setting to `False` to display categories list instead of threads list on board index.


## `MISAGO_THREADS_PER_PAGE`

Controls number of threads displayed on page. Greater numbers can increase number of objects loaded into memory and thus depending on features enabled greatly increase memory usage.


## `MISAGO_THREADS_TAIL`

Defines minimal number of threads for lists last page. If number of threads on last page is smaller or equal to one specified in this setting, last page will be appended to previous page instead.


## `MISAGO_THREAD_TYPES`

List of clasess defining thread types.


## `MISAGO_USE_STOP_FORUM_SPAM`

This settings allows you to decide wheter of not [Stop Forum Spam](http://www.stopforumspam.com/) database should be used to validate IPs and emails during new users registrations.


## `MISAGO_USERS_PER_PAGE`

Controls pagination of users lists.
