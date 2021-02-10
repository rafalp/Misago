from unittest.mock import MagicMock, patch

import pytest

from bh.core_utils.test_utils import ServiceCallMock, mock_service_call
from bh_settings import get_settings

from community_app.posting.middleware import RiskWordsMiddleware


@pytest.fixture
def user():
    mock = MagicMock(username="abcdef")
    mock.social_auth.get.return_value.uid = "a1b2c3"
    return mock


@patch("community_app.posting.middleware.mail")
@mock_service_call(
    ServiceCallMock(
        "RiskWords", "1", "evaluate_text_for_risk_words", return_value={"is_safe": False, "distress_words_found": ["risk"], "swear_words_found": []}
    )
)
def test_post_save_unsafe(_mocks, mail_mock, user):
    middleware = RiskWordsMiddleware(user=user, thread=MagicMock(title="title"), post=MagicMock(original="test message with a risk word"))
    middleware.post_save(None)

    expected_body = (
        f"Risk Words detected in a Community Post\n"
        + f"User UUID: a1b2c3\n"
        + f"Community Username: abcdef\n"
        + f"Thread Title: title\n"
        + f"Post: test message with a risk word\n"
        + f"Distress Words Found: ['risk']\n"
        + f"Swear Words Found: []"
    )
    expected_subject = f"Risk Words detected in a Community Post - {get_settings('stage')}"
    mail_mock.send_mail.assert_called_with(
        subject=expected_subject, message=expected_body, from_email="engineering@bighealth.com", recipient_list=["communityadmin@sleepio.com"]
    )

@patch("community_app.posting.middleware.mail")
@mock_service_call(
    ServiceCallMock(
        "RiskWords", "1", "evaluate_text_for_risk_words", return_value={"is_safe": True, "distress_words_found": [], "swear_words_found": []}
    )
)
def test_post_save_safe(_mocks, mail_mock, user):
    middleware = RiskWordsMiddleware(user=user, thread=MagicMock(title="title"), post=MagicMock(original="test message with a risk word"))
    middleware.post_save(None)

    mail_mock.send_mail.assert_not_called()
