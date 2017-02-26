import requests

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from misago.conf import settings


def recaptcha_test(request):
    r = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.recaptcha_secret_key,
            'response': request.data.get('captcha'),
            'remoteip': request.user_ip
        }
    )

    if r.status_code == 200:
        response_json = r.json()
        if not response_json.get('success'):
            raise ValidationError(_("Please try again."))
    else:
        raise ValidationError(_("Failed to contact reCAPTCHA API."))


def qacaptcha_test(request):
    answer = request.data.get('captcha', '').lower()
    for predefined_answer in settings.qa_answers.lower().splitlines():
        predefined_answer = predefined_answer.strip().lower()
        if answer == predefined_answer:
            break
    else:
        raise ValidationError(_("Entered answer is incorrect."))


def nocaptcha_test(request):
    return  # no captcha means no validation


CAPTCHA_TESTS = {
    're': recaptcha_test,
    'qa': qacaptcha_test,
    'no': nocaptcha_test,
}


def test_request(request):
    CAPTCHA_TESTS[settings.captcha_type](request)
