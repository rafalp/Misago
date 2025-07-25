# Built-in hooks reference

This document contains a list of all standard plugin hooks existing in Misago.

Hooks instances are importable from the following Python modules:

- [`misago.attachments.hooks`](#misago-attachments-hooks)
- [`misago.categories.hooks`](#misago-categories-hooks)
- [`misago.oauth2.hooks`](#misago-oauth2-hooks)
- [`misago.parser.hooks`](#misago-parser-hooks)
- [`misago.permissions.hooks`](#misago-permissions-hooks)
- [`misago.polls.hooks`](#misago-polls-hooks)
- [`misago.posting.hooks`](#misago-posting-hooks)
- [`misago.threads.hooks`](#misago-threads-hooks)
- [`misago.threadupdates.hooks`](#misago-threadupdates-hooks)
- [`misago.users.hooks`](#misago-users-hooks)


## `misago.attachments.hooks`

`misago.attachments.hooks` defines the following hooks:

- [`delete_attachments_hook`](./delete-attachments-hook.md)
- [`delete_categories_attachments_hook`](./delete-categories-attachments-hook.md)
- [`delete_posts_attachments_hook`](./delete-posts-attachments-hook.md)
- [`delete_threads_attachments_hook`](./delete-threads-attachments-hook.md)
- [`delete_users_attachments_hook`](./delete-users-attachments-hook.md)
- [`get_attachment_details_page_context_data_hook`](./get-attachment-details-page-context-data-hook.md)
- [`get_attachment_plugin_data_hook`](./get-attachment-plugin-data-hook.md)
- [`serialize_attachment_hook`](./serialize-attachment-hook.md)


## `misago.categories.hooks`

`misago.categories.hooks` defines the following hooks:

- [`delete_categories_hook`](./delete-categories-hook.md)
- [`get_categories_page_component_hook`](./get-categories-page-component-hook.md)
- [`get_categories_page_metatags_hook`](./get-categories-page-metatags-hook.md)
- [`get_categories_query_values_hook`](./get-categories-query-values-hook.md)
- [`get_category_data_hook`](./get-category-data-hook.md)


## `misago.oauth2.hooks`

`misago.oauth2.hooks` defines the following hooks:

- [`filter_user_data_hook`](./filter-user-data-hook.md)
- [`validate_user_data_hook`](./validate-user-data-hook.md)


## `misago.parser.hooks`

`misago.parser.hooks` defines the following hooks:

- [`create_parser_hook`](./create-parser-hook.md)
- [`get_tokens_metadata_hook`](./get-tokens-metadata-hook.md)
- [`highlight_syntax_hook`](./highlight-syntax-hook.md)
- [`render_tokens_to_plaintext_hook`](./render-tokens-to-plaintext-hook.md)
- [`replace_rich_text_tokens_hook`](./replace-rich-text-tokens-hook.md)
- [`shorten_url_hook`](./shorten-url-hook.md)
- [`tokenize_hook`](./tokenize-hook.md)


## `misago.permissions.hooks`

`misago.permissions.hooks` defines the following hooks:

- [`build_user_category_permissions_hook`](./build-user-category-permissions-hook.md)
- [`build_user_permissions_hook`](./build-user-permissions-hook.md)
- [`can_upload_private_threads_attachments_hook`](./can-upload-private-threads-attachments-hook.md)
- [`can_upload_threads_attachments_hook`](./can-upload-threads-attachments-hook.md)
- [`check_access_category_permission_hook`](./check-access-category-permission-hook.md)
- [`check_access_post_permission_hook`](./check-access-post-permission-hook.md)
- [`check_access_thread_permission_hook`](./check-access-thread-permission-hook.md)
- [`check_browse_category_permission_hook`](./check-browse-category-permission-hook.md)
- [`check_close_thread_poll_permission_hook`](./check-close-thread-poll-permission-hook.md)
- [`check_delete_attachment_permission_hook`](./check-delete-attachment-permission-hook.md)
- [`check_delete_thread_poll_permission_hook`](./check-delete-thread-poll-permission-hook.md)
- [`check_download_attachment_permission_hook`](./check-download-attachment-permission-hook.md)
- [`check_edit_private_thread_permission_hook`](./check-edit-private-thread-permission-hook.md)
- [`check_edit_private_thread_post_permission_hook`](./check-edit-private-thread-post-permission-hook.md)
- [`check_edit_thread_permission_hook`](./check-edit-thread-permission-hook.md)
- [`check_edit_thread_poll_permission_hook`](./check-edit-thread-poll-permission-hook.md)
- [`check_edit_thread_post_permission_hook`](./check-edit-thread-post-permission-hook.md)
- [`check_open_thread_poll_permission_hook`](./check-open-thread-poll-permission-hook.md)
- [`check_post_in_closed_category_permission_hook`](./check-post-in-closed-category-permission-hook.md)
- [`check_post_in_closed_thread_permission_hook`](./check-post-in-closed-thread-permission-hook.md)
- [`check_private_threads_permission_hook`](./check-private-threads-permission-hook.md)
- [`check_reply_private_thread_permission_hook`](./check-reply-private-thread-permission-hook.md)
- [`check_reply_thread_permission_hook`](./check-reply-thread-permission-hook.md)
- [`check_see_category_permission_hook`](./check-see-category-permission-hook.md)
- [`check_see_private_thread_permission_hook`](./check-see-private-thread-permission-hook.md)
- [`check_see_private_thread_post_permission_hook`](./check-see-private-thread-post-permission-hook.md)
- [`check_see_thread_permission_hook`](./check-see-thread-permission-hook.md)
- [`check_see_thread_post_permission_hook`](./check-see-thread-post-permission-hook.md)
- [`check_start_poll_permission_hook`](./check-start-poll-permission-hook.md)
- [`check_start_private_threads_permission_hook`](./check-start-private-threads-permission-hook.md)
- [`check_start_thread_permission_hook`](./check-start-thread-permission-hook.md)
- [`check_start_thread_poll_permission_hook`](./check-start-thread-poll-permission-hook.md)
- [`check_vote_in_thread_poll_permission_hook`](./check-vote-in-thread-poll-permission-hook.md)
- [`copy_category_permissions_hook`](./copy-category-permissions-hook.md)
- [`copy_group_permissions_hook`](./copy-group-permissions-hook.md)
- [`filter_accessible_thread_posts_hook`](./filter-accessible-thread-posts-hook.md)
- [`filter_private_thread_posts_queryset_hook`](./filter-private-thread-posts-queryset-hook.md)
- [`filter_private_thread_updates_queryset_hook`](./filter-private-thread-updates-queryset-hook.md)
- [`filter_private_threads_queryset_hook`](./filter-private-threads-queryset-hook.md)
- [`filter_thread_posts_queryset_hook`](./filter-thread-posts-queryset-hook.md)
- [`filter_thread_updates_queryset_hook`](./filter-thread-updates-queryset-hook.md)
- [`get_admin_category_permissions_hook`](./get-admin-category-permissions-hook.md)
- [`get_category_threads_category_query_hook`](./get-category-threads-category-query-hook.md)
- [`get_category_threads_pinned_category_query_hook`](./get-category-threads-pinned-category-query-hook.md)
- [`get_category_threads_query_hook`](./get-category-threads-query-hook.md)
- [`get_threads_category_query_hook`](./get-threads-category-query-hook.md)
- [`get_threads_pinned_category_query_hook`](./get-threads-pinned-category-query-hook.md)
- [`get_threads_query_orm_filter_hook`](./get-threads-query-orm-filter-hook.md)
- [`get_user_permissions_hook`](./get-user-permissions-hook.md)


## `misago.polls.hooks`

`misago.polls.hooks` defines the following hooks:

- [`close_poll_hook`](./close-poll-hook.md)
- [`close_thread_poll_hook`](./close-thread-poll-hook.md)
- [`delete_poll_hook`](./delete-poll-hook.md)
- [`delete_thread_poll_hook`](./delete-thread-poll-hook.md)
- [`edit_thread_poll_hook`](./edit-thread-poll-hook.md)
- [`open_poll_hook`](./open-poll-hook.md)
- [`open_thread_poll_hook`](./open-thread-poll-hook.md)
- [`save_thread_poll_hook`](./save-thread-poll-hook.md)
- [`validate_poll_choices_hook`](./validate-poll-choices-hook.md)
- [`validate_poll_question_hook`](./validate-poll-question-hook.md)


## `misago.posting.hooks`

`misago.posting.hooks` defines the following hooks:

- [`get_edit_private_thread_formset_hook`](./get-edit-private-thread-formset-hook.md)
- [`get_edit_private_thread_post_formset_hook`](./get-edit-private-thread-post-formset-hook.md)
- [`get_edit_private_thread_post_state_hook`](./get-edit-private-thread-post-state-hook.md)
- [`get_edit_thread_formset_hook`](./get-edit-thread-formset-hook.md)
- [`get_edit_thread_post_formset_hook`](./get-edit-thread-post-formset-hook.md)
- [`get_edit_thread_post_state_hook`](./get-edit-thread-post-state-hook.md)
- [`get_reply_private_thread_formset_hook`](./get-reply-private-thread-formset-hook.md)
- [`get_reply_private_thread_state_hook`](./get-reply-private-thread-state-hook.md)
- [`get_reply_thread_formset_hook`](./get-reply-thread-formset-hook.md)
- [`get_reply_thread_state_hook`](./get-reply-thread-state-hook.md)
- [`get_start_private_thread_formset_hook`](./get-start-private-thread-formset-hook.md)
- [`get_start_private_thread_state_hook`](./get-start-private-thread-state-hook.md)
- [`get_start_thread_formset_hook`](./get-start-thread-formset-hook.md)
- [`get_start_thread_state_hook`](./get-start-thread-state-hook.md)
- [`post_needs_content_upgrade_hook`](./post-needs-content-upgrade-hook.md)
- [`save_edit_private_thread_post_state_hook`](./save-edit-private-thread-post-state-hook.md)
- [`save_edit_thread_post_state_hook`](./save-edit-thread-post-state-hook.md)
- [`save_reply_private_thread_state_hook`](./save-reply-private-thread-state-hook.md)
- [`save_reply_thread_state_hook`](./save-reply-thread-state-hook.md)
- [`save_start_private_thread_state_hook`](./save-start-private-thread-state-hook.md)
- [`save_start_thread_state_hook`](./save-start-thread-state-hook.md)
- [`upgrade_post_code_blocks_hook`](./upgrade-post-code-blocks-hook.md)
- [`upgrade_post_content_hook`](./upgrade-post-content-hook.md)
- [`validate_post_hook`](./validate-post-hook.md)
- [`validate_posted_contents_hook`](./validate-posted-contents-hook.md)
- [`validate_thread_title_hook`](./validate-thread-title-hook.md)


## `misago.threads.hooks`

`misago.threads.hooks` defines the following hooks:

- [`create_prefetch_posts_feed_related_objects_hook`](./create-prefetch-posts-feed-related-objects-hook.md)
- [`get_category_threads_page_context_data_hook`](./get-category-threads-page-context-data-hook.md)
- [`get_category_threads_page_filters_hook`](./get-category-threads-page-filters-hook.md)
- [`get_category_threads_page_moderation_actions_hook`](./get-category-threads-page-moderation-actions-hook.md)
- [`get_category_threads_page_queryset_hook`](./get-category-threads-page-queryset-hook.md)
- [`get_category_threads_page_subcategories_hook`](./get-category-threads-page-subcategories-hook.md)
- [`get_category_threads_page_threads_hook`](./get-category-threads-page-threads-hook.md)
- [`get_edit_private_thread_page_context_data_hook`](./get-edit-private-thread-page-context-data-hook.md)
- [`get_edit_private_thread_post_page_context_data_hook`](./get-edit-private-thread-post-page-context-data-hook.md)
- [`get_edit_thread_page_context_data_hook`](./get-edit-thread-page-context-data-hook.md)
- [`get_edit_thread_post_page_context_data_hook`](./get-edit-thread-post-page-context-data-hook.md)
- [`get_private_thread_replies_page_context_data_hook`](./get-private-thread-replies-page-context-data-hook.md)
- [`get_private_thread_replies_page_posts_queryset_hook`](./get-private-thread-replies-page-posts-queryset-hook.md)
- [`get_private_thread_replies_page_thread_queryset_hook`](./get-private-thread-replies-page-thread-queryset-hook.md)
- [`get_private_threads_page_context_data_hook`](./get-private-threads-page-context-data-hook.md)
- [`get_private_threads_page_filters_hook`](./get-private-threads-page-filters-hook.md)
- [`get_private_threads_page_queryset_hook`](./get-private-threads-page-queryset-hook.md)
- [`get_private_threads_page_threads_hook`](./get-private-threads-page-threads-hook.md)
- [`get_redirect_to_post_response_hook`](./get-redirect-to-post-response-hook.md)
- [`get_reply_private_thread_page_context_data_hook`](./get-reply-private-thread-page-context-data-hook.md)
- [`get_reply_thread_page_context_data_hook`](./get-reply-thread-page-context-data-hook.md)
- [`get_start_private_thread_page_context_data_hook`](./get-start-private-thread-page-context-data-hook.md)
- [`get_start_thread_page_context_data_hook`](./get-start-thread-page-context-data-hook.md)
- [`get_thread_replies_page_context_data_hook`](./get-thread-replies-page-context-data-hook.md)
- [`get_thread_replies_page_posts_queryset_hook`](./get-thread-replies-page-posts-queryset-hook.md)
- [`get_thread_replies_page_thread_queryset_hook`](./get-thread-replies-page-thread-queryset-hook.md)
- [`get_thread_url_hook`](./get-thread-url-hook.md)
- [`get_threads_page_context_data_hook`](./get-threads-page-context-data-hook.md)
- [`get_threads_page_filters_hook`](./get-threads-page-filters-hook.md)
- [`get_threads_page_moderation_actions_hook`](./get-threads-page-moderation-actions-hook.md)
- [`get_threads_page_queryset_hook`](./get-threads-page-queryset-hook.md)
- [`get_threads_page_subcategories_hook`](./get-threads-page-subcategories-hook.md)
- [`get_threads_page_threads_hook`](./get-threads-page-threads-hook.md)
- [`set_posts_feed_related_objects_hook`](./set-posts-feed-related-objects-hook.md)


## `misago.threadupdates.hooks`

`misago.threadupdates.hooks` defines the following hooks:

- [`create_thread_update_hook`](./create-thread-update-hook.md)
- [`delete_thread_update_hook`](./delete-thread-update-hook.md)
- [`hide_thread_update_hook`](./hide-thread-update-hook.md)
- [`unhide_thread_update_hook`](./unhide-thread-update-hook.md)


## `misago.users.hooks`

`misago.users.hooks` defines the following hooks:

- [`create_group_hook`](./create-group-hook.md)
- [`delete_group_hook`](./delete-group-hook.md)
- [`set_default_group_hook`](./set-default-group-hook.md)
- [`update_group_description_hook`](./update-group-description-hook.md)
- [`update_group_hook`](./update-group-hook.md)