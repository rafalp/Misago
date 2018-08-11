# -*- coding: utf-8 -*-
from path import Path

from django.core.exceptions import ValidationError
from django.test import TestCase

from misago.conf import settings
from misago.core.utils import slugify

from misago.users.avatars import dynamic
from misago.users.models import Avatar, User


class UserManagerTests(TestCase):
    def test_create_user(self):
        """create_user created new user account successfully"""
        user = User.objects.create_user(
            'Bob',
            'bob@test.com',
            'Pass.123',
            set_default_avatar=True,
        )

        db_user = User.objects.get(id=user.pk)

        self.assertEqual(user.username, db_user.username)
        self.assertEqual(user.slug, db_user.slug)
        self.assertEqual(user.email, db_user.email)
        self.assertEqual(user.email_hash, db_user.email_hash)

    def test_create_user_twice(self):
        """create_user is raising validation error for duplicate users"""
        User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')
        with self.assertRaises(ValidationError):
            User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

    def test_create_superuser(self):
        """create_superuser created new user account successfully"""
        user = User.objects.create_superuser('Bob', 'bob@test.com', 'Pass.123')

        db_user = User.objects.get(id=user.pk)

        self.assertTrue(user.is_staff)
        self.assertTrue(db_user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(db_user.is_superuser)

    def test_get_user(self):
        """get_by_ methods return user correctly"""
        user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        db_user = User.objects.get_by_username(user.username)
        self.assertEqual(user.pk, db_user.pk)

        db_user = User.objects.get_by_email(user.email)
        self.assertEqual(user.pk, db_user.pk)

        db_user = User.objects.get_by_username_or_email(user.username)
        self.assertEqual(user.pk, db_user.pk)

        db_user = User.objects.get_by_username_or_email(user.email)
        self.assertEqual(user.pk, db_user.pk)

    def test_getters_unicode_handling(self):
        """get_by_ methods handle unicode"""
        with self.assertRaises(User.DoesNotExist):
            User.objects.get_by_username(u'łóć')

        with self.assertRaises(User.DoesNotExist):
            User.objects.get_by_email(u'łóć@polskimail.pl')

        with self.assertRaises(User.DoesNotExist):
            User.objects.get_by_username_or_email(u'łóć@polskimail.pl')


class UserModelTests(TestCase):
    def test_anonymize_data(self):
        """anonymize_data sets username and slug to one defined in settings"""
        user = User.objects.create_user('Bob', 'bob@example.com', 'Pass.123')

        user.anonymize_data()
        self.assertEqual(user.username, settings.MISAGO_ANONYMOUS_USERNAME)
        self.assertEqual(user.slug, slugify(settings.MISAGO_ANONYMOUS_USERNAME))

    def test_delete_avatar_on_delete(self):
        """account deletion for user also deletes their avatar file"""
        user = User.objects.create_user('Bob', 'bob@example.com', 'Pass.123')
        dynamic.set_avatar(user)
        user.save()

        user_avatars = []
        for avatar in user.avatar_set.all():
            avatar_path = Path(avatar.image.path)
            self.assertTrue(avatar_path.exists())
            self.assertTrue(avatar_path.isfile())
            user_avatars.append(avatar)
        self.assertNotEqual(user_avatars, [])
        
        user.delete()

        for removed_avatar in user_avatars:
            avatar_path = Path(removed_avatar.image.path)
            self.assertFalse(avatar_path.exists())
            self.assertFalse(avatar_path.isfile())

            with self.assertRaises(Avatar.DoesNotExist):
                Avatar.objects.get(pk=removed_avatar.pk)

    def test_set_username(self):
        """set_username sets username and slug on model"""
        user = User()

        user.set_username('Boberson')
        self.assertEqual(user.username, 'Boberson')
        self.assertEqual(user.slug, 'boberson')

        self.assertEqual(user.get_username(), 'Boberson')
        self.assertEqual(user.get_full_name(), 'Boberson')
        self.assertEqual(user.get_short_name(), 'Boberson')

    def test_set_email(self):
        """set_email sets email and hash on model"""
        user = User()

        user.set_email('bOb@TEst.com')
        self.assertEqual(user.email, 'bOb@test.com')
        self.assertTrue(user.email_hash)

    def test_mark_for_delete(self):
        """mark_for_delete deactivates user and sets is_deleting_account flag"""
        user = User.objects.create_user('Bob', 'bob@example.com', 'Pass.123')
        user.mark_for_delete()
        self.assertFalse(user.is_active)
        self.assertTrue(user.is_deleting_account)

        user_from_db = User.objects.get(pk=user.pk)
        self.assertFalse(user_from_db.is_active)
        self.assertTrue(user_from_db.is_deleting_account)

    def test_get_real_name(self):
        """get_real_name returns user-set real name or none"""
        user = User.objects.create_user('Bob', 'bob@example.com', 'Pass.123')
        self.assertIsNone(user.get_real_name())

        user.profile_fields['real_name'] = 'Bob Boberson'
        self.assertEqual(user.get_real_name(), 'Bob Boberson')
