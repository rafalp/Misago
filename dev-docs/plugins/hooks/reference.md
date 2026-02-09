# Built-in hooks reference

This document contains a list of all standard plugin hooks existing in Misago.

Hooks instances are importable from the following Python modules:

- [`misago.attachments.hooks`](#misago-attachments-hooks)
- [`misago.categories.hooks`](#misago-categories-hooks)
- [`misago.edits.hooks`](#misago-edits-hooks)
- [`misago.likes.hooks`](#misago-likes-hooks)
- [`misago.notifications.hooks`](#misago-notifications-hooks)
- [`misago.oauth2.hooks`](#misago-oauth2-hooks)
- [`misago.parser.hooks`](#misago-parser-hooks)
- [`misago.permissions.hooks`](#misago-permissions-hooks)
- [`misago.polls.hooks`](#misago-polls-hooks)
- [`misago.posting.hooks`](#misago-posting-hooks)
- [`misago.privatethreads.hooks`](#misago-privatethreads-hooks)
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


## `misago.edits.hooks`

`misago.edits.hooks` defines the following hooks:

- [`create_post_edit_hook`](./create-post-edit-hook.md)
- [`delete_post_edit_hook`](./delete-post-edit-hook.md)
- [`get_private_thread_post_edits_view_context_data_hook`](./get-private-thread-post-edits-view-context-data-hook.md)
- [`get_thread_post_edits_view_context_data_hook`](./get-thread-post-edits-view-context-data-hook.md)
- [`hide_post_edit_hook`](./hide-post-edit-hook.md)
- [`restore_post_edit_hook`](./restore-post-edit-hook.md)
- [`unhide_post_edit_hook`](./unhide-post-edit-hook.md)


## `misago.likes.hooks`

`misago.likes.hooks` defines the following hooks:

- [`get_post_feed_post_likes_data_hook`](./get-post-feed-post-likes-data-hook.md)
- [`like_post_hook`](./like-post-hook.md)
- [`remove_post_like_hook`](./remove-post-like-hook.md)
- [`synchronize_post_likes_hook`](./synchronize-post-likes-hook.md)


## `misago.notifications.hooks`

`misago.notifications.hooks` defines the following hooks:

- [`unwatch_thread_hook`](./unwatch-thread-hook.md)
- [`watch_thread_hook`](./watch-thread-hook.md)


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
- [`can_see_post_edit_count_hook`](./can-see-post-edit-count-hook.md)
- [`can_see_post_likes_count_hook`](./can-see-post-likes-count-hook.md)
- [`can_upload_private_threads_attachments_hook`](./can-upload-private-threads-attachments-hook.md)
- [`can_upload_threads_attachments_hook`](./can-upload-threads-attachments-hook.md)
- [`check_access_category_permission_hook`](./check-access-category-permission-hook.md)
- [`check_access_post_permission_hook`](./check-access-post-permission-hook.md)
- [`check_access_thread_permission_hook`](./check-access-thread-permission-hook.md)
- [`check_browse_category_permission_hook`](./check-browse-category-permission-hook.md)
- [`check_change_private_thread_owner_permission_hook`](./check-change-private-thread-owner-permission-hook.md)
- [`check_close_thread_poll_permission_hook`](./check-close-thread-poll-permission-hook.md)
- [`check_delete_attachment_permission_hook`](./check-delete-attachment-permission-hook.md)
- [`check_delete_post_edit_permission_hook`](./check-delete-post-edit-permission-hook.md)
- [`check_delete_thread_poll_permission_hook`](./check-delete-thread-poll-permission-hook.md)
- [`check_download_attachment_permission_hook`](./check-download-attachment-permission-hook.md)
- [`check_edit_private_thread_permission_hook`](./check-edit-private-thread-permission-hook.md)
- [`check_edit_private_thread_post_permission_hook`](./check-edit-private-thread-post-permission-hook.md)
- [`check_edit_thread_permission_hook`](./check-edit-thread-permission-hook.md)
- [`check_edit_thread_poll_permission_hook`](./check-edit-thread-poll-permission-hook.md)
- [`check_edit_thread_post_permission_hook`](./check-edit-thread-post-permission-hook.md)
- [`check_hide_post_edit_permission_hook`](./check-hide-post-edit-permission-hook.md)
- [`check_like_post_permission_hook`](./check-like-post-permission-hook.md)
- [`check_locked_category_permission_hook`](./check-locked-category-permission-hook.md)
- [`check_locked_private_thread_permission_hook`](./check-locked-private-thread-permission-hook.md)
- [`check_locked_thread_permission_hook`](./check-locked-thread-permission-hook.md)
- [`check_open_thread_poll_permission_hook`](./check-open-thread-poll-permission-hook.md)
- [`check_private_threads_permission_hook`](./check-private-threads-permission-hook.md)
- [`check_remove_private_thread_member_permission_hook`](./check-remove-private-thread-member-permission-hook.md)
- [`check_reply_private_thread_permission_hook`](./check-reply-private-thread-permission-hook.md)
- [`check_reply_thread_permission_hook`](./check-reply-thread-permission-hook.md)
- [`check_restore_post_edit_permission_hook`](./check-restore-post-edit-permission-hook.md)
- [`check_see_category_permission_hook`](./check-see-category-permission-hook.md)
- [`check_see_post_edit_history_permission_hook`](./check-see-post-edit-history-permission-hook.md)
- [`check_see_post_likes_permission_hook`](./check-see-post-likes-permission-hook.md)
- [`check_see_private_thread_permission_hook`](./check-see-private-thread-permission-hook.md)
- [`check_see_private_thread_post_permission_hook`](./check-see-private-thread-post-permission-hook.md)
- [`check_see_thread_permission_hook`](./check-see-thread-permission-hook.md)
- [`check_see_thread_post_permission_hook`](./check-see-thread-post-permission-hook.md)
- [`check_start_poll_permission_hook`](./check-start-poll-permission-hook.md)
- [`check_start_private_threads_permission_hook`](./check-start-private-threads-permission-hook.md)
- [`check_start_thread_permission_hook`](./check-start-thread-permission-hook.md)
- [`check_start_thread_poll_permission_hook`](./check-start-thread-poll-permission-hook.md)
- [`check_unhide_post_edit_permission_hook`](./check-unhide-post-edit-permission-hook.md)
- [`check_unlike_post_permission_hook`](./check-unlike-post-permission-hook.md)
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

- [`get_private_thread_edit_context_data_hook`](./get-private-thread-edit-context-data-hook.md)
- [`get_private_thread_edit_formset_hook`](./get-private-thread-edit-formset-hook.md)
- [`get_private_thread_post_edit_context_data_hook`](./get-private-thread-post-edit-context-data-hook.md)
- [`get_private_thread_post_edit_formset_hook`](./get-private-thread-post-edit-formset-hook.md)
- [`get_private_thread_post_edit_state_hook`](./get-private-thread-post-edit-state-hook.md)
- [`get_private_thread_reply_context_data_hook`](./get-private-thread-reply-context-data-hook.md)
- [`get_private_thread_reply_formset_hook`](./get-private-thread-reply-formset-hook.md)
- [`get_private_thread_reply_state_hook`](./get-private-thread-reply-state-hook.md)
- [`get_private_thread_start_context_data_hook`](./get-private-thread-start-context-data-hook.md)
- [`get_private_thread_start_formset_hook`](./get-private-thread-start-formset-hook.md)
- [`get_private_thread_start_state_hook`](./get-private-thread-start-state-hook.md)
- [`get_thread_edit_context_data_hook`](./get-thread-edit-context-data-hook.md)
- [`get_thread_edit_formset_hook`](./get-thread-edit-formset-hook.md)
- [`get_thread_post_edit_context_data_hook`](./get-thread-post-edit-context-data-hook.md)
- [`get_thread_post_edit_formset_hook`](./get-thread-post-edit-formset-hook.md)
- [`get_thread_post_edit_state_hook`](./get-thread-post-edit-state-hook.md)
- [`get_thread_reply_context_data_hook`](./get-thread-reply-context-data-hook.md)
- [`get_thread_reply_formset_hook`](./get-thread-reply-formset-hook.md)
- [`get_thread_reply_state_hook`](./get-thread-reply-state-hook.md)
- [`get_thread_start_context_data_hook`](./get-thread-start-context-data-hook.md)
- [`get_thread_start_formset_hook`](./get-thread-start-formset-hook.md)
- [`get_thread_start_state_hook`](./get-thread-start-state-hook.md)
- [`post_needs_content_upgrade_hook`](./post-needs-content-upgrade-hook.md)
- [`save_private_thread_post_edit_state_hook`](./save-private-thread-post-edit-state-hook.md)
- [`save_private_thread_reply_state_hook`](./save-private-thread-reply-state-hook.md)
- [`save_private_thread_start_state_hook`](./save-private-thread-start-state-hook.md)
- [`save_thread_post_edit_state_hook`](./save-thread-post-edit-state-hook.md)
- [`save_thread_reply_state_hook`](./save-thread-reply-state-hook.md)
- [`save_thread_start_state_hook`](./save-thread-start-state-hook.md)
- [`upgrade_post_code_blocks_hook`](./upgrade-post-code-blocks-hook.md)
- [`upgrade_post_content_hook`](./upgrade-post-content-hook.md)
- [`validate_post_hook`](./validate-post-hook.md)
- [`validate_posted_contents_hook`](./validate-posted-contents-hook.md)
- [`validate_thread_title_hook`](./validate-thread-title-hook.md)


## `misago.privatethreads.hooks`

`misago.privatethreads.hooks` defines the following hooks:

- [`change_private_thread_owner_hook`](./change-private-thread-owner-hook.md)
- [`get_private_thread_detail_view_context_data_hook`](./get-private-thread-detail-view-context-data-hook.md)
- [`get_private_thread_detail_view_posts_queryset_hook`](./get-private-thread-detail-view-posts-queryset-hook.md)
- [`get_private_thread_detail_view_thread_queryset_hook`](./get-private-thread-detail-view-thread-queryset-hook.md)
- [`get_private_thread_list_context_data_hook`](./get-private-thread-list-context-data-hook.md)
- [`get_private_thread_list_filters_hook`](./get-private-thread-list-filters-hook.md)
- [`get_private_thread_list_queryset_hook`](./get-private-thread-list-queryset-hook.md)
- [`get_private_thread_list_threads_hook`](./get-private-thread-list-threads-hook.md)
- [`remove_private_thread_member_hook`](./remove-private-thread-member-hook.md)
- [`validate_new_private_thread_member_hook`](./validate-new-private-thread-member-hook.md)
- [`validate_new_private_thread_owner_hook`](./validate-new-private-thread-owner-hook.md)


## `misago.threads.hooks`

`misago.threads.hooks` defines the following hooks:

- [`create_prefetch_post_feed_related_objects_hook`](./create-prefetch-post-feed-related-objects-hook.md)
- [`get_category_threads_page_context_data_hook`](./get-category-threads-page-context-data-hook.md)
- [`get_category_threads_page_filters_hook`](./get-category-threads-page-filters-hook.md)
- [`get_category_threads_page_moderation_actions_hook`](./get-category-threads-page-moderation-actions-hook.md)
- [`get_category_threads_page_queryset_hook`](./get-category-threads-page-queryset-hook.md)
- [`get_category_threads_page_subcategories_hook`](./get-category-threads-page-subcategories-hook.md)
- [`get_category_threads_page_threads_hook`](./get-category-threads-page-threads-hook.md)
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
- [`move_threads_hook`](./move-threads-hook.md)
- [`set_post_feed_related_objects_hook`](./set-post-feed-related-objects-hook.md)
- [`synchronize_thread_hook`](./synchronize-thread-hook.md)


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