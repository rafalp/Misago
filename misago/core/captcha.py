from recaptcha.client.captcha import displayhtml, submit as submit_recaptcha
from django.utils.translation import ugettext_lazy as _

from misago.conf import settings
from misago.core import forms


def add_captcha_to_form(FormType, request):
    captcha_type = settings.captcha_on_registration
    test_passed = session_already_passed_test(request.session)

    captcha_attrs = {}
    if captcha_type == 'recaptcha':
        captcha_attrs.update(add_recaptcha_to_form(request, test_passed))
    elif captcha_type == 'qa':
        captcha_attrs.update(add_qa_test_to_form(request, test_passed))

    if captcha_attrs:
        captcha_attrs['session'] = request.session

    return type('FinalRegisterForm', (FormType,), captcha_attrs)


"""
reCaptcha
"""
def clean_recaptcha(self):
    if not self.data.get('recaptcha_response_field'):
        raise forms.ValidationError(_("This field is required."))

    api_response = submit_recaptcha(
        self.data.get('recaptcha_challenge_field'),
        self.data.get('recaptcha_response_field'),
        settings.recaptcha_private_api_key,
        self._misago_real_ip)

    if api_response.is_valid:
        self.has_recaptcha = False
        mark_session_as_passing(self.session)
    else:
        raise forms.ValidationError(_("Text from image is incorrect."))

    return ''


def add_recaptcha_to_form(request, test_passed):
    recaptcha_field = forms.CharField(label=_('Security image'),
                                      required=False)
    field_html = displayhtml(settings.recaptcha_public_api_key,
                             request.is_secure())

    extra_fields = {
        'passed_recaptcha': test_passed,
        'has_recaptcha': True,
        'recaptcha': recaptcha_field,
        'recaptcha_html': field_html,
        '_misago_real_ip': request._misago_real_ip,
        'clean_recaptcha': clean_recaptcha,
    }

    if test_passed:
        extra_fields['has_recaptcha'] = False
        extra_fields.pop('clean_recaptcha')

    return extra_fields


"""
Q&A
"""
def clean_qa_answer(self):
    answer = self.cleaned_data['qa_answer'].lower()

    for predefined_answer in settings.qa_answers.lower().splitlines():
        predefined_answer = predefined_answer.strip().lower()
        if answer == predefined_answer:
            self.has_qa_captcha = False
            mark_session_as_passing(self.session)
            return self.cleaned_data['qa_answer']
    else:
        raise forms.ValidationError(_("Entered answer is incorrect."))


def add_qa_test_to_form(request, test_passed):
    qa_answer_field = forms.CharField(label=settings.qa_question,
                                      help_text=settings.qa_help_text,
                                      required=(not test_passed))

    extra_fields = {
        'passed_qa_captcha': test_passed,
        'has_qa_captcha': True,
        'qa_answer': qa_answer_field,
        'clean_qa_answer': clean_qa_answer,
    }

    if test_passed:
        extra_fields['has_qa_captcha'] = False
        extra_fields.pop('clean_qa_answer')

    return extra_fields


"""
Session utils
"""
def session_already_passed_test(session):
    return session.get('passes_captcha')


def mark_session_as_passing(session):
    session['passes_captcha'] = True
