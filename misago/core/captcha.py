from django.utils.translation import ugettext_lazy as _
from misago.conf import settings
from misago.core import forms


def add_captcha_to_form(FormType, request):
    if session_already_passed_test(request.session):
        return FormType
    else:
        captcha_attrs = {}

        captcha_type = getattr(settings, FormType.captcha_setting)
        if captcha_type == 'recaptcha':
            captcha_attrs['has_recaptcha'] = True
            captcha_attrs.update(add_recaptcha_to_form(request))
        elif captcha_type == 'qa':
            captcha_attrs['has_qa_captcha'] = True
            captcha_attrs.update(add_qa_test_to_form(request))

        if captcha_attrs:
            captcha_attrs['session'] = request.session
        return type('FinalRegisterForm', (FormType,), captcha_attrs)


"""
reCaptcha
"""
def add_recaptcha_to_form(request):
    extra_fields = {}
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
        raise forms.ValidationError(_("Entered answer is invalid."))


def add_qa_test_to_form(request):
    qa_answer_field = forms.CharField(label=settings.qa_question,
                                      help_text=settings.qa_help_text)

    extra_fields = {
        'qa_answer': qa_answer_field,
        'clean_qa_answer': clean_qa_answer,
    }
    return extra_fields


"""
Session utils
"""
def session_already_passed_test(session):
    return session.get('passes_captcha')


def mark_session_as_passing(session):
    session['passes_captcha'] = True
