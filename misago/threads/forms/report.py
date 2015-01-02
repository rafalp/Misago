from django.utils.translation import ugettext_lazy as _
from misago.core import forms


class ReportPostForm(forms.Form):
    report_message = forms.CharField(label=_("Optional report message"),
                                     widget=forms.Textarea(attrs={'rows': 3}),
                                     required=False)

    def clean_report_message(self):
        data = self.cleaned_data['report_message']
        if len(data) > 2000:
            raise forms.ValidationError("Report message cannot be "
                                        "longer than 2000 characters.")
        return data
