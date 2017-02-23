# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.test import TestCase

from misago.users.models import User


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
