(function () {
  'use strict';

  window.initTestMisago = function() {
    var misago = new Misago();

    var context = {
      "CSRF_COOKIE_NAME": "csrftoken",

      "STATIC_URL": "/dist/",
      "MEDIA_URL": "/media/",

      "SETTINGS": {
        "LOGIN_URL": "/login/",
        "LOGIN_API_URL": "auth",
        "LOGIN_REDIRECT_URL": "/",
        "LOGOUT_URL": "/logout/",

        "thread_title_length_min": 5,
        "account_activation": "none",
        "recaptcha_site_key": "",
        "password_length_min": 5,
        "forum_branding_text": "isago",
        "username_length_max": 14,
        "signature_length_max": 256,
        "username_length_min": 3,
        "forum_footnote": "",
        "forum_index_title": "Misago Preview",
        "captcha_type": "no",
        "forum_branding_display": true,
        "forum_name": "Misago",
        "avatar_upload_limit": 750,
        "thread_title_length_max": 90,

        "privacy_policy": true,
        "privacy_policy_title": "Test Privacy Policy",
        "privacy_policy_link": "",

        "terms_of_service": true,
        "terms_of_service_title": "Test Terms",
        "terms_of_service_link": ""
      },

      "isAuthenticated": false,
      "user": {
        "id": null,
        "acl": {
          "can_delete_users_newer_than": 0,
          "can_see_users_name_history": 0,
          "can_moderate_avatars": 0,
          "can_be_warned": 1,
          "can_see_reports": [],
          "can_follow_users": 0,
          "can_see_users_emails": 0,
          "can_see_users_online_list": 0,
          "can_moderate_signatures": 0,
          "can_start_private_threads": 0,
          "name_changes_allowed": 0,
          "can_add_everyone_to_private_threads": 0,
          "_acl_version": 6,
          "can_rename_users": 0,
          "can_browse_users_list": 1,
          "allow_signature_links": 0,
          "visible_forums": [3, 4, 5],
          "can_warn_users": 0,
          "can_report_private_threads": 0,
          "can_search_users": 1,
          "can_use_private_threads": 0,
          "can_be_blocked": 1,
          "can_review_moderated_content": [],
          "can_delete_users_with_less_posts_than": 0,
          "can_moderate_private_threads": 0,
          "can_see_ban_details": 0,
          "can_delete_warnings": 0,
          "can_see_users_ips": 0,
          "allow_signature_blocks": 0,
          "can_ban_users": 0,
          "max_ban_length": 2,
          "can_have_signature": 0,
          "allow_signature_images": 0,
          "can_see_hidden_users": 0,
          "max_private_thread_participants": 3,
          "can_cancel_warnings": 0,
          "name_changes_expire": 0,
          "can_lift_bans": 0,
          "max_lifted_ban_length": 2,
          "can_see_other_users_warnings": 0
        }
      }
    };

    misago.init({
      test: true,
      fixture: 'misago-fixture',
      api: '/test-api/'
    }, context);

    return misago;
  };
}());
