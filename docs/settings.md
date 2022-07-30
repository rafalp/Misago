Settings reference
==================

In Misago there are two types of settings: static settings that are initialized on Misago startup and don't change afterwards, and dynamic settings that are stored in database and can be changed from admin control panel.


Static settings
---------------

Static settings values are accessible throught the attributes of `misago.conf.settings` object:

- `debug: bool` - Switch controlling if `debug` mode is enabled.
- `test: bool` - Switch specifying if application is running within test runner (pytest).
- `test_database_name: Optional[str]` - If specified, makes tests run against different database.
- `database_url: str` - Database connection URL as used by [`Databases` library](https://www.encode.io/databases/database_queries/).
- `cache_url: str` - Cache connection URL as used by [`async-caches` library](https://rafalp.github.io/async-caches/backends/).
- `static_root: str` - Absolute path to directory from which static files are served by the HTTP server.
- `media_root: str` - Absolute path to directory from which uploaded files are served by the HTTP server.
- `avatar_sizes: List[int]` - List of user avatar sizes supported on site. Env variable should be comma separated list: `40, 100, 400`.
- `enabled_plugins: Optional[str]` - Absolute path to text file with a list of enabled plugins.


Dynamic settings
----------------

- `avatar_upload_max_size: int` - Limit of uploaded image file size, in kilobytes.
- `bulk_action_limit: int` - Maximum allowed number of items in bulk action (close threads, delete users).
- `enable_site_wizard: bool` - Controls if site wizard UI and `setupSite` graphQL mutations are available.
- `forum_index_header: str` - Header text on forum index.
- `forum_index_threads: bool` - If `True`, display threads list on forum index. Categories otherwise.
- `forum_index_title: str` - Page title on forum index.
- `forum_name: str` - Forum name.
- `jwt_exp: int` - Time for which JWT tokens stay valid, in seconds.
- `jwt_secret: str` - JWT secret. Should be at least 64 characters long to be secure.
- `password_min_length: int` - Min. allowed password length.
- `post_min_length: int` - Min. required length of post body.
- `posts_per_page: int` - Number of posts displayed per page on thread view.
- `posts_per_page_orphans: int` - Max. number of orphaned posts that should rolled up to previous page.
- `thread_title_min_length: int` - Min. required length of thread title.
- `thread_title_max_length: int` - Max. allowed length of thread title.
- `threads_per_page: int` - Max number of threads displayed on single page of threads list.
- `username_max_length: int` - Min. allowed username length.
- `username_min_length: int` - Max. allowed username length.