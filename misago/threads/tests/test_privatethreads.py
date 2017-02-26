from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.users.testutils import AuthenticatedUserTestCase


class PrivateThreadsTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(PrivateThreadsTestCase, self).setUp()
        self.category = Category.objects.private_threads()

        override_acl(self.user, {
            'can_use_private_threads': 1,
            'can_start_private_threads': 1,
        })

        self.override_acl()

    def override_acl(self, acl=None):
        final_acl = self.user.acl_cache['categories'][self.category.pk]
        final_acl.update({
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_see_own_threads': 0,
            'can_hide_threads': 0,
            'can_approve_content': 0,
            'can_edit_posts': 0,
            'can_hide_posts': 0,
            'can_hide_own_posts': 0,
            'can_merge_threads': 0,
        })

        if acl:
            final_acl.update(acl)

        override_acl(self.user, {
            'categories': {
                self.category.pk: final_acl,
            },
        })
