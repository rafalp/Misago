from bh_settings import get_settings
from bh.services.factory import Factory

from django.core import mail
from misago.threads.api.postingendpoint import PostingMiddleware


class RiskWordsMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        return get_settings("enable_risk_words_notifications", True)

    def post_save(self, serializer):
        risk_words_service = Factory.create("RiskWords", "1")
        text = f"{str(self.thread.title)} {str(self.post.original)}"
        response = risk_words_service.evaluate_text_for_risk_words(text=text)
        if not response["is_safe"]:
            body = (
                f"Risk Words detected in a Community Post\n"
                + f"User UUID: {self.user.social_auth.get(provider='sleepio').uid}\n"
                + f"Community Username: {self.user.username}\n"
                + f"Thread Title: {self.thread.title}\n"
                + f"Post: {self.post.original}\n"
                + f"Distress Words Found: {response['distress_words_found']}\n"
                + f"Swear Words Found: {response['swear_words_found']}"
            )
            mail.send_mail(
                subject=f"Risk Words detected in a Community Post - {get_settings('stage')}",
                message=body,
                from_email="engineering@bighealth.com",
                recipient_list=get_settings("risk_words_emails"),
            )
