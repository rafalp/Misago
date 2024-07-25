# Built-in hooks reference

This document contains a list of all standard plugin hooks existing in Misago.

Hooks instances are importable from the following Python modules:

- [`misago.categories.hooks`](#misago-categories-hooks)
- [`misago.oauth2.hooks`](#misago-oauth2-hooks)
- [`misago.parser.hooks`](#misago-parser-hooks)
- [`misago.permissions.hooks`](#misago-permissions-hooks)
- [`misago.threads.hooks`](#misago-threads-hooks)
- [`misago.users.hooks`](#misago-users-hooks)


## `misago.categories.hooks`

`misago.categories.hooks` defines the following hooks:



## `misago.oauth2.hooks`

`misago.oauth2.hooks` defines the following hooks:

- [`filter_user_data_hook`](./filter-user-data-hook.md)
- [`validate_user_data_hook`](./validate-user-data-hook.md)


## `misago.parser.hooks`

`misago.parser.hooks` defines the following hooks:

- [`complete_markup_html_hook`](./complete-markup-html-hook.md)
- [`create_parser_hook`](./create-parser-hook.md)
- [`get_ast_metadata_users_queryset_hook`](./get-ast-metadata-users-queryset-hook.md)
- [`render_ast_node_to_html_hook`](./render-ast-node-to-html-hook.md)
- [`render_ast_node_to_plaintext_hook`](./render-ast-node-to-plaintext-hook.md)
- [`setup_parser_context_hook`](./setup-parser-context-hook.md)
- [`update_ast_metadata_from_node_hook`](./update-ast-metadata-from-node-hook.md)
- [`update_ast_metadata_hook`](./update-ast-metadata-hook.md)
- [`update_ast_metadata_users_hook`](./update-ast-metadata-users-hook.md)


## `misago.permissions.hooks`

`misago.permissions.hooks` defines the following hooks:

- [`build_user_category_permissions_hook`](./build-user-category-permissions-hook.md)
- [`build_user_permissions_hook`](./build-user-permissions-hook.md)
- [`copy_category_permissions_hook`](./copy-category-permissions-hook.md)
- [`copy_group_permissions_hook`](./copy-group-permissions-hook.md)
- [`get_admin_category_permissions_hook`](./get-admin-category-permissions-hook.md)
- [`get_category_threads_category_query_hook`](./get-category-threads-category-query-hook.md)
- [`get_category_threads_pinned_category_query_hook`](./get-category-threads-pinned-category-query-hook.md)
- [`get_threads_category_query_hook`](./get-threads-category-query-hook.md)
- [`get_threads_pinned_category_query_hook`](./get-threads-pinned-category-query-hook.md)
- [`get_threads_query_orm_filter_hook`](./get-threads-query-orm-filter-hook.md)
- [`get_user_permissions_hook`](./get-user-permissions-hook.md)


## `misago.threads.hooks`

`misago.threads.hooks` defines the following hooks:

- [`get_category_threads_page_context_hook`](./get-category-threads-page-context-hook.md)
- [`get_category_threads_page_filters_hook`](./get-category-threads-page-filters-hook.md)
- [`get_category_threads_page_moderation_actions_hook`](./get-category-threads-page-moderation-actions-hook.md)
- [`get_category_threads_page_queryset_hook`](./get-category-threads-page-queryset-hook.md)
- [`get_category_threads_page_subcategories_hook`](./get-category-threads-page-subcategories-hook.md)
- [`get_category_threads_page_threads_hook`](./get-category-threads-page-threads-hook.md)
- [`get_private_threads_page_context_hook`](./get-private-threads-page-context-hook.md)
- [`get_private_threads_page_filters_hook`](./get-private-threads-page-filters-hook.md)
- [`get_private_threads_page_queryset_hook`](./get-private-threads-page-queryset-hook.md)
- [`get_private_threads_page_threads_hook`](./get-private-threads-page-threads-hook.md)
- [`get_threads_page_context_hook`](./get-threads-page-context-hook.md)
- [`get_threads_page_filters_hook`](./get-threads-page-filters-hook.md)
- [`get_threads_page_moderation_actions_hook`](./get-threads-page-moderation-actions-hook.md)
- [`get_threads_page_queryset_hook`](./get-threads-page-queryset-hook.md)
- [`get_threads_page_subcategories_hook`](./get-threads-page-subcategories-hook.md)
- [`get_threads_page_threads_hook`](./get-threads-page-threads-hook.md)


## `misago.users.hooks`

`misago.users.hooks` defines the following hooks:

- [`create_group_hook`](./create-group-hook.md)
- [`delete_group_hook`](./delete-group-hook.md)
- [`set_default_group_hook`](./set-default-group-hook.md)
- [`update_group_description_hook`](./update-group-description-hook.md)
- [`update_group_hook`](./update-group-hook.md)