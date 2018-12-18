from misago.categories.models import Category
from misago.users.testutils import AuthenticatedUserTestCase


class PrivateThreadsTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.private_threads()
