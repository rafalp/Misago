from recaptcha.client.captcha import displayhtml, submit as submit_recaptcha
from django.utils.translation import ugettext_lazy as _

from misago.conf import settings
from misago.core import forms


def validate_recaptcha(request):
    raise NotImplementedError('reCaptcha 2 is not implemented')
    answer = self.cleaned_data['qa_answer'].lower()

    for predefined_answer in settings.qa_answers.lower().splitlines():
        predefined_answer = predefined_answer.strip().lower()
        if answer == predefined_answer:
            self.has_qa_captcha = False
            return self.cleaned_data['qa_answer']
    else:
        raise forms.ValidationError(_("Entered answer is incorrect."))


def validate_qacaptcha(request):
    raise NotImplementedError('Q&A captcha is not implemented')


def validate_nocaptcha(request):
    return # no captcha means no validation


CAPTCHA_TESTS = {
    're': validate_recaptcha,
    'qa': validate_qacaptcha,
    'no': validate_nocaptcha,
}

def validate_captcha(request):
    if not session_already_passed_test(request.session):
        # run test and if it didn't raise validation error,
        # mark session as passing so we don't troll uses anymore
        CAPTCHA_TESTS[settings['captcha_type']](request)
        mark_session_as_passing(request.session)


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
    return session.get('passed_captcha')


def mark_session_as_passing(session):
    session['passed_captcha'] = True
