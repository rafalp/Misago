from misago.models import Role
from misago.utils.translation import ugettext_lazy as _

def load():
    role = Role(name=_("Administrator").message, _special='admin', protected=True)
    role.permissions = {
                        'name_changes_allowed': 5,
                        'changes_expire': 7,
                        'can_search_forums': True,
                        'search_cooldown': 0,
                        'can_use_acp': True,
                        'can_use_signature': True,
                        'allow_signature_links': True,
                        'allow_signature_images': True,
                        'can_search_users': True,
                        'can_see_users_emails': True,
                        'can_see_users_trails': True,
                        'can_see_hidden_users': True,
                        'can_use_private_threads': True,
                        'can_start_private_threads': True,
                        'can_upload_attachments_in_private_threads': True,
                        'private_thread_attachment_size': 0,
                        'private_thread_attachments_limit': 0,
                        'can_invite_ignoring': True,
                        'private_threads_mod': True,
                        'can_delete_checkpoints': 2,
                        'can_report_content': True,
                        'can_handle_reports': True,
                        'can_mod_reports_discussions': True,
                        'can_delete_reports': True,
                        'forums': {3: 1, 5: 1, 6: 1},
                        'can_destroy_user_newer_than': 14,
                        'can_destroy_users_with_less_posts_than': 10,
                       }
    role.save(force_insert=True)

    role = Role(name=_("Moderator").message, _special='mod', protected=True)
    role.permissions = {
                        'name_changes_allowed': 3,
                        'changes_expire': 14,
                        'can_search_forums': True,
                        'search_cooldown': 0,
                        'can_use_signature': True,
                        'allow_signature_links': True,
                        'can_search_users': True,
                        'can_see_users_emails': True,
                        'can_see_users_trails': True,
                        'can_see_hidden_users': True,
                        'can_use_private_threads': True,
                        'can_start_private_threads': True,
                        'can_upload_attachments_in_private_threads': True,
                        'private_thread_attachment_size': 500,
                        'private_thread_attachments_limit': 4,
                        'can_invite_ignoring': True,
                        'private_threads_mod': True,
                        'can_delete_checkpoints': 1,
                        'can_report_content': True,
                        'can_handle_reports': True,
                        'forums': {3: 1, 5: 1, 6: 1},
                        'can_destroy_user_newer_than': 5,
                        'can_destroy_users_with_less_posts_than': 10,
                       }
    role.save(force_insert=True)

    role = Role(name=_("Registered").message, _special='registered')
    role.permissions = {
                        'name_changes_allowed': 2,
                        'can_search_forums': True,
                        'search_cooldown': 20,
                        'can_use_signature': False,
                        'can_search_users': True,
                        'can_use_private_threads': True,
                        'can_start_private_threads': True,
                        'can_upload_attachments_in_private_threads': False,
                        'private_thread_attachment_size': 100,
                        'private_thread_attachments_limit': 3,
                        'can_invite_ignoring': False,
                        'private_threads_mod': False,
                        'can_report_content': True,
                        'forums': {4: 3, 5: 3, 6: 3},
                       }
    role.save(force_insert=True)

    role = Role(name=_("Guest").message, _special='guest')
    role.permissions = {
                        'can_search_forums': True,
                        'search_cooldown': 45,
                        'can_search_users': True,
                        'forums': {4: 6, 5: 6, 6: 6},
                       }
    role.save(force_insert=True)