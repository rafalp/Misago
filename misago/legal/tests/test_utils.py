from django.test import TestCase

from misago.legal.models import Agreement, UserAgreement
from misago.legal.utils import (
    get_parsed_agreement_text, get_required_user_agreement, save_user_agreement_acceptance,
    set_agreement_as_active
)
from misago.users.testutils import UserTestCase


class MockRequest(object):
    def __init__(self, user=None):
        self.user = user
        self.frontend_context = {}

    def get_host(self):
        return 'testhost.com'


class GetParsedAgreementTextTests(TestCase):
    def test_agreement_no_text(self):
        agreement = Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            link='https://somewhre.com',
            is_active=True,
        )

        result = get_parsed_agreement_text(MockRequest(), agreement)
        self.assertIsNone(result)

    def test_agreement_link_and_text(self):
        agreement = Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            link='https://somewhre.com',
            text='Lorem ipsum',
            is_active=True,
        )

        result = get_parsed_agreement_text(MockRequest(), agreement)
        self.assertEqual(result, '<p>Lorem ipsum</p>')

    def test_agreement_text(self):
        agreement = Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            text='Lorem ipsum',
            is_active=True,
        )

        result = get_parsed_agreement_text(MockRequest(), agreement)
        self.assertEqual(result, '<p>Lorem ipsum</p>')


class GetRequiredUserAgreementTests(UserTestCase):
    def setUp(self):
        self.agreement = Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            link='https://somewhre.com',
            text='Lorem ipsum',
            is_active=True,
        )

        self.agreements = Agreement.objects.get_agreements_from_db()

    def test_anonymous_user(self):
        anonymous_user = self.get_anonymous_user()
        result = get_required_user_agreement(anonymous_user, self.agreements)
        self.assertIsNone(result)

    def test_authenticated_user_no_agreements(self):
        authenticated_user = self.get_authenticated_user()
        result = get_required_user_agreement(authenticated_user, {})
        self.assertIsNone(result)

    def test_authenticated_user(self):
        authenticated_user = self.get_authenticated_user()
        result = get_required_user_agreement(authenticated_user, self.agreements)
        self.assertEqual(result, self.agreement)

    def test_authenticated_user_with_agreement(self):
        authenticated_user = self.get_authenticated_user()
        authenticated_user.agreements.append(self.agreement.pk)

        result = get_required_user_agreement(authenticated_user, self.agreements)
        self.assertIsNone(result)

    def test_prioritize_terms_of_service(self):
        terms_of_service = Agreement.objects.create(
            type=Agreement.TYPE_TOS,
            link='https://somewhre.com',
            text='Lorem ipsum',
            is_active=True,
        )

        agreements = Agreement.objects.get_agreements_from_db()
        agreements_in_wrong_order = {
            Agreement.TYPE_PRIVACY: agreements[Agreement.TYPE_PRIVACY],
            Agreement.TYPE_TOS: agreements[Agreement.TYPE_TOS],
        }

        authenticated_user = self.get_authenticated_user()
        result = get_required_user_agreement(authenticated_user, agreements_in_wrong_order)
        self.assertEqual(result, terms_of_service)


class SaveUserAgreementAcceptance(UserTestCase):
    def test_no_commit(self):
        user = self.get_authenticated_user()

        agreement = Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            link='https://somewhre.com',
            text='Lorem ipsum',
        )

        save_user_agreement_acceptance(user, agreement)
        self.assertEqual(user.agreements, [agreement.id])

        user.refresh_from_db()
        self.assertEqual(user.agreements, [])

        UserAgreement.objects.get(user=user, agreement=agreement)
        self.assertEqual(UserAgreement.objects.count(), 1)

    def test_commit(self):
        user = self.get_authenticated_user()

        agreement = Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            link='https://somewhre.com',
            text='Lorem ipsum',
        )

        save_user_agreement_acceptance(user, agreement, commit=True)
        self.assertEqual(user.agreements, [agreement.id])

        user.refresh_from_db()
        self.assertEqual(user.agreements, [agreement.id])

        UserAgreement.objects.get(user=user, agreement=agreement)
        self.assertEqual(UserAgreement.objects.count(), 1)


class SetAgreementAsActiveTests(TestCase):
     def test_inactive_agreement(self):
        agreement = Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            link='https://somewhre.com',
            text='Lorem ipsum',
        )

        set_agreement_as_active(agreement)
        self.assertTrue(agreement.is_active)

        agreement.refresh_from_db()
        self.assertFalse(agreement.is_active)

     def test_inactive_agreement_commit(self):
        agreement = Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            link='https://somewhre.com',
            text='Lorem ipsum',
        )

        set_agreement_as_active(agreement, commit=True)
        self.assertTrue(agreement.is_active)

        agreement.refresh_from_db()
        self.assertTrue(agreement.is_active)
        
     def test_change_active_agreement(self):
        old_agreement = Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            link='https://somewhre.com',
            text='Lorem ipsum',
            is_active=True,
        )

        new_agreement = Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            link='https://somewhre.com',
            text='Lorem ipsum',
        )

        other_type_agreement = Agreement.objects.create(
            type=Agreement.TYPE_TOS,
            link='https://somewhre.com',
            text='Lorem ipsum',
            is_active=True,
        )

        set_agreement_as_active(new_agreement, commit=True)

        old_agreement.refresh_from_db()
        new_agreement.refresh_from_db()
        other_type_agreement.refresh_from_db()

        self.assertFalse(old_agreement.is_active)
        self.assertTrue(new_agreement.is_active)
        self.assertTrue(other_type_agreement.is_active)
