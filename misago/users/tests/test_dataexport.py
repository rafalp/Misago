from misago.users.dataexport import is_user_data_export_in_progress, start_data_export_for_user
from misago.users.models import DataExport
from misago.users.testutils import AuthenticatedUserTestCase


class IsUserDataExportInProgressTests(AuthenticatedUserTestCase):
    def test_util_returns_false_for_no_export(self):
        """is_user_data_export_in_progress returns false if user has no export in progress"""
        self.assertFalse(is_user_data_export_in_progress(self.user))

    def test_util_returns_false_for_ready_export(self):
        """is_user_data_export_in_progress returns false if user has ready export"""
        data_export = start_data_export_for_user(self.user)
        data_export.status = DataExport.STATUS_READY
        data_export.save()

        self.assertFalse(is_user_data_export_in_progress(self.user))

    def test_util_returns_false_for_expired_export(self):
        """is_user_data_export_in_progress returns false if user has expired export"""
        data_export = start_data_export_for_user(self.user)
        data_export.status = DataExport.STATUS_EXPIRED
        data_export.save()
        
        self.assertFalse(is_user_data_export_in_progress(self.user))

    def test_util_returns_true_for_pending_export(self):
        """is_user_data_export_in_progress returns true if user has pending export"""
        data_export = start_data_export_for_user(self.user)
        data_export.status = DataExport.STATUS_PENDING
        data_export.save()
        
        self.assertTrue(is_user_data_export_in_progress(self.user))

    def test_util_returns_true_for_processing_export(self):
        """is_user_data_export_in_progress returns true if user has processing export"""
        data_export = start_data_export_for_user(self.user)
        data_export.status = DataExport.STATUS_PROCESSING
        data_export.save()
        
        self.assertTrue(is_user_data_export_in_progress(self.user))


class StartDataExportForUserTests(AuthenticatedUserTestCase):
    def test_util_creates_data_export_for_user_with_them_as_requester(self):
        """start_data_export_for_user created valid data export for user"""
        data_export = start_data_export_for_user(self.user)

        self.assertEqual(data_export.user, self.user)
        self.assertEqual(data_export.requester, self.user)
        self.assertEqual(data_export.requester_name, self.user.username)
        self.assertEqual(data_export.status, DataExport.STATUS_PENDING)

    def test_util_creates_data_export_for_user_explicit_requester(self):
        """start_data_export_for_user created valid data export for user with other requester"""
        requester = self.get_superuser()
        data_export = start_data_export_for_user(self.user, requester)

        self.assertEqual(data_export.user, self.user)
        self.assertEqual(data_export.requester, requester)
        self.assertEqual(data_export.requester_name, requester.username)
        self.assertEqual(data_export.status, DataExport.STATUS_PENDING)
