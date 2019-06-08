from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from ..audittrail import create_audit_trail, create_user_audit_trail
from ..models import AuditTrail
from ..signals import remove_old_ips
from ..test import UserTestCase, create_test_user

User = get_user_model()

USER_IP = "13.41.51.41"


class MockRequest:
    user_ip = USER_IP

    def __init__(self, user):
        self.user = user


class CreateAuditTrailTests(UserTestCase):
    def setUp(self):
        super().setUp()

        self.obj = create_test_user("OtherUser", "user@example.com")

    def test_create_audit_require_model(self):
        """create_audit_trail requires model instance"""
        anonymous_user = self.get_anonymous_user()
        request = MockRequest(anonymous_user)
        with self.assertRaises(ValueError):
            create_audit_trail(request, anonymous_user)
        self.assertEqual(AuditTrail.objects.count(), 0)

    def test_create_audit_trail_anonymous_user(self):
        """create_audit_trail doesn't record anonymous users"""
        user = self.get_anonymous_user()
        request = MockRequest(user)
        create_audit_trail(request, self.obj)
        self.assertEqual(AuditTrail.objects.count(), 0)

    def test_create_audit_trail(self):
        """create_audit_trail creates new db record"""
        user = self.get_authenticated_user()
        request = MockRequest(user)
        create_audit_trail(request, self.obj)
        self.assertEqual(AuditTrail.objects.count(), 1)

        audit_trail = user.audittrail_set.all()[0]
        self.assertEqual(audit_trail.user, user)
        self.assertEqual(audit_trail.ip_address, request.user_ip)
        self.assertEqual(audit_trail.content_object, self.obj)

    def test_delete_user_remove_audit_trail(self):
        """audit trail is deleted together with user it belongs to"""
        user = self.get_authenticated_user()
        request = MockRequest(user)
        create_audit_trail(request, self.obj)
        self.assertEqual(AuditTrail.objects.count(), 1)

        user.delete()
        self.assertEqual(AuditTrail.objects.count(), 0)

    def test_delete_obj_keep_audit_trail(self):
        """audit trail is kept after with obj it points at is deleted"""
        user = self.get_authenticated_user()
        request = MockRequest(user)
        create_audit_trail(request, self.obj)
        self.assertEqual(AuditTrail.objects.count(), 1)

        self.obj.delete()
        self.assertEqual(AuditTrail.objects.count(), 1)

        audit_trail = user.audittrail_set.all()[0]
        self.assertEqual(audit_trail.user, user)
        self.assertEqual(audit_trail.ip_address, request.user_ip)
        self.assertIsNone(audit_trail.content_object)

    def test_delete_audit_trail(self):
        """audit trail deletion leaves other data untouched"""
        user = self.get_authenticated_user()
        request = MockRequest(user)
        create_audit_trail(request, self.obj)
        self.assertEqual(AuditTrail.objects.count(), 1)

        audit_trail = user.audittrail_set.all()[0]
        audit_trail.delete()

        User.objects.get(id=user.id)
        User.objects.get(id=self.obj.id)


class CreateUserAuditTrailTests(UserTestCase):
    def setUp(self):
        super().setUp()

        self.obj = create_test_user("OtherUser", "user@example.com")

    def test_create_user_audit_require_model(self):
        """create_user_audit_trail requires model instance"""
        anonymous_user = self.get_anonymous_user()
        with self.assertRaises(ValueError):
            create_user_audit_trail(anonymous_user, USER_IP, anonymous_user)
        self.assertEqual(AuditTrail.objects.count(), 0)

    def test_create_user_audit_trail_anonymous_user(self):
        """create_user_audit_trail doesn't record anonymous users"""
        user = self.get_anonymous_user()
        create_user_audit_trail(user, USER_IP, self.obj)
        self.assertEqual(AuditTrail.objects.count(), 0)

    def test_create_user_audit_trail(self):
        """create_user_audit_trail creates new db record"""
        user = self.get_authenticated_user()
        create_user_audit_trail(user, USER_IP, self.obj)
        self.assertEqual(AuditTrail.objects.count(), 1)

        audit_trail = user.audittrail_set.all()[0]
        self.assertEqual(audit_trail.user, user)
        self.assertEqual(audit_trail.ip_address, USER_IP)
        self.assertEqual(audit_trail.content_object, self.obj)

    def test_delete_user_remove_audit_trail(self):
        """audit trail is deleted together with user it belongs to"""
        user = self.get_authenticated_user()
        create_user_audit_trail(user, USER_IP, self.obj)
        self.assertEqual(AuditTrail.objects.count(), 1)

        user.delete()
        self.assertEqual(AuditTrail.objects.count(), 0)

    def test_delete_obj_keep_audit_trail(self):
        """audit trail is kept after with obj it points at is deleted"""
        user = self.get_authenticated_user()
        create_user_audit_trail(user, USER_IP, self.obj)
        self.assertEqual(AuditTrail.objects.count(), 1)

        self.obj.delete()
        self.assertEqual(AuditTrail.objects.count(), 1)

        audit_trail = user.audittrail_set.all()[0]
        self.assertEqual(audit_trail.user, user)
        self.assertEqual(audit_trail.ip_address, USER_IP)
        self.assertIsNone(audit_trail.content_object)

    def test_delete_audit_trail(self):
        """audit trail deletion leaves other data untouched"""
        user = self.get_authenticated_user()
        create_user_audit_trail(user, USER_IP, self.obj)
        self.assertEqual(AuditTrail.objects.count(), 1)

        audit_trail = user.audittrail_set.all()[0]
        audit_trail.delete()

        User.objects.get(id=user.id)
        User.objects.get(id=self.obj.id)


def test_recent_audit_trail_is_not_deleted(user, other_user):
        create_user_audit_trail(user, USER_IP, other_user)
        remove_old_ips.send(None, ip_storage_time=1)
        assert user.audittrail_set.exists()
    

def test_old_audit_trail_is_deleted(user, other_user):
        audit_trail = create_user_audit_trail(user, USER_IP, other_user)
        audit_trail.created_on = timezone.now() - timedelta(days=6)
        audit_trail.save()

        remove_old_ips.send(None, ip_storage_time=5)
        assert not user.audittrail_set.exists()
