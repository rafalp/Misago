(function () {
  'use strict';

  window.mockUser = function(properties) {
    var user = {
      "id": 42,
      "username": "BobBoberson",
      "slug": "bobboberson",
      "email": "bob@example.com",
      "joined_on": "2015-05-04T20:16:41.084500Z",
      "is_hiding_presence": false,
      "title": null,
      "full_title": "Forum team",
      "short_title": "Team",
      "rank": {
          "id": 1,
          "name": "Forum team",
          "slug": "forum-team",
          "description": null,
          "title": "Team",
          "css_class": "team",
          "is_tab": true
      },
      "avatar_hash": 'a0b9c8d7',
      "new_notifications": 0,
      "limits_private_thread_invites_to": 0,
      "unread_private_threads": 0,
      "sync_unread_private_threads": false,
      "subscribe_to_started_threads": 2,
      "subscribe_to_replied_threads": 2,
      "threads": 0,
      "posts": 0,
      "acl": {
          "can_delete_users_newer_than": 3,
          "can_see_users_name_history": 1,
          "can_moderate_avatars": 1,
          "can_be_warned": 0,
          "can_see_reports": [
              3,
              4,
              5
          ],
          "can_follow_users": 1,
          "can_see_users_emails": 1,
          "can_see_users_online_list": 1,
          "can_moderate_signatures": 1,
          "can_start_private_threads": 1,
          "name_changes_allowed": 5,
          "can_add_everyone_to_private_threads": 1,
          "_acl_version": 0,
          "can_rename_users": 0,
          "can_browse_users_list": 1,
          "allow_signature_links": 1,
          "visible_forums": [
              3,
              4,
              5
          ],
          "can_warn_users": 1,
          "can_report_private_threads": 1,
          "can_search_users": 1,
          "can_use_private_threads": 1,
          "can_be_blocked": 0,
          "can_review_moderated_content": [
              3,
              4,
              5,
              1
          ],
          "can_delete_users_with_less_posts_than": 7,
          "can_moderate_private_threads": 1,
          "can_see_ban_details": 1,
          "can_delete_warnings": 0,
          "can_see_users_ips": 1,
          "allow_signature_blocks": 0,
          "can_ban_users": 0,
          "max_ban_length": 2,
          "can_have_signature": 1,
          "allow_signature_images": 0,
          "can_see_hidden_users": 1,
          "max_private_thread_participants": 15,
          "can_cancel_warnings": 1,
          "name_changes_expire": 0,
          "can_lift_bans": 0,
          "max_lifted_ban_length": 2,
          "can_see_other_users_warnings": 1
      }
    };

    if (properties) {
      return $.extend(user, properties);
    } else {
      return user;
    }
  };
}());
