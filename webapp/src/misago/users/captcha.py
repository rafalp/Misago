import requests
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def recaptcha_test(request):
    r = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            "secret": request.settings.recaptcha_secret_key,
            "response": request.data.get("captcha"),
            "remoteip": request.user_ip,
        },
    )

    if r.status_code == 200:
        response_json = r.json()
        if not response_json.get("success"):
            raise ValidationError(_("Please try again."))
    else:
        raise ValidationError(_("Failed to contact reCAPTCHA API."))


def qacaptcha_test(request):
    answer = request.data.get("captcha", "").lower().strip()
    valid_answers = get_valid_qacaptcha_answers(request.settings)
    if answer not in valid_answers:
        raise ValidationError(_("Entered answer is incorrect."))


def get_valid_qacaptcha_answers(settings):
    valid_answers = [i.strip() for i in settings.qa_answers.lower().splitlines()]
    return filter(len, valid_answers)


def nocaptcha_test(request):
    return  # no captcha means no validation


CAPTCHA_TESTS = {"re": recaptcha_test, "qa": qacaptcha_test, "no": nocaptcha_test}


def test_request(request):
    CAPTCHA_TESTS[request.settings.captcha_type](request)
