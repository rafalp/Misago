from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.users import tokens


UserModel = get_user_model()


class TokensTests(TestCase):
    def test_tokens(self):
        """misago.users.tokens implementation works"""
        user_a = UserModel.objects.create_user('Bob', 'bob@test.com', 'ogasiM200_')
        user_b = UserModel.objects.create_user('Weebl', 'weebl@test.com', 'ogasiM200_')

        token_a = tokens.make(user_a, 'test')
        token_b = tokens.make(user_b, 'test')

        self.assertTrue(tokens.is_valid(user_a, 'test', token_a))
        self.assertTrue(tokens.is_valid(user_b, 'test', token_b))
        self.assertTrue(token_a != token_b)
