from ...categories.models import Category
from ...users.test import AuthenticatedUserTestCase


class PrivateThreadsTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.private_threads()
