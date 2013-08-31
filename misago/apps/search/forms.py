from django.utils import timezone
from django.utils.translation import ungettext_lazy, ugettext_lazy as _
import floppyforms as forms
from misago.forms import Form, ForumMultipleChoiceField
from misago.models import Forum

class SearchFormBase(Form):
    search_query = forms.CharField(label=_("Search Phrases"), max_length=255)
    search_thread_titles = forms.BooleanField(label=_("Search Thread Titles"), required=False)
    search_thread = forms.CharField(label=_("Thread Name or Link"),
                                    help_text=_("Limit search to specified thread by entering it's name or link here."),
                                    max_length=255,
                                    required=False)
    search_author = forms.CharField(label=_("Author Name"),
                                    help_text=_("Limit search to specified user by entering his or her name here."),
                                    max_length=255,
                                    required=False)

    def clean_search_query(self):
        data = self.cleaned_data['search_query']
        if len(data) < 3:
            raise forms.ValidationError(_("Search query should be at least 3 characters long."))
        return data

    def clean(self):
        cleaned_data = super(SearchFormBase, self).clean()
        if self.request.user.is_authenticated():
            self.check_flood_user()
        if self.request.user.is_anonymous():
            self.check_flood_guest()
        return cleaned_data

    def check_flood_user(self):
        if self.request.user.last_search:
            diff = timezone.now() - self.request.user.last_search
            diff = diff.seconds + (diff.days * 86400)
            wait_for = self.request.acl.search.search_cooldown() - diff
            if wait_for > 0:
                if wait_for < 5:
                    raise forms.ValidationError(_("You can't perform one search so quickly after another. Please wait a moment and try again."))
                else:
                    raise forms.ValidationError(ungettext_lazy(
                            "You can't perform one search so quickly after another. Please wait %(seconds)d second and try again.",
                            "You can't perform one search so quickly after another. Please wait %(seconds)d seconds and try again.",
                        wait_for) % {
                            'seconds': wait_for,
                        })

    def check_flood_guest(self):
        if not self.request.session.matched:
            raise forms.ValidationError(_("Search requires enabled cookies in order to work."))

        if self.request.session.get('last_search'):
            diff = timezone.now() - self.request.session.get('last_search')
            diff = diff.seconds + (diff.days * 86400)
            wait_for = self.request.acl.search.search_cooldown() - diff
            if wait_for > 0:
                if wait_for < 5:
                    raise forms.ValidationError(_("You can't perform one search so quickly after another. Please wait a moment and try again."))
                else:
                    raise forms.ValidationError(ungettext_lazy(
                            "You can't perform one search so quickly after another. Please wait %(seconds)d second and try again.",
                            "You can't perform one search so quickly after another. Please wait %(seconds)d seconds and try again.",
                        wait_for) % {
                            'seconds': wait_for,
                        })


class QuickSearchForm(SearchFormBase):
    pass


class AdvancedSearchForm(SearchFormBase):
    search_before = forms.DateField(label=_("Posted Before"),
                                    help_text=_("Exclude posts made before specified date from search. Use YYYY-MM-DD format, for example 2013-11-23."),
                                    required=False)
    search_after = forms.DateField(label=_("Posted After"),
                                   help_text=_("Exclude posts made after specified date from search. Use YYYY-MM-DD format, for example 2013-11-23."),
                                   required=False)


class ForumsSearchForm(AdvancedSearchForm):
    def finalize_form(self):
        self.add_field('search_forums', ForumMultipleChoiceField(label=_("Search Forums"),
                                                                 help_text=_("If you want, you can limit search to specified forums."),
                                                                 queryset=Forum.objects.get(special='root').get_descendants().filter(pk__in=self.request.acl.forums.acl['can_browse']),
                                                                 required=False, empty_label=None, widget=forms.SelectMultiple))
        self.add_field('search_forums_childs', forms.BooleanField(label=_("Include Children Forums"), required=False))


class PrivateThreadsSearchForm(AdvancedSearchForm):
    pass


class ReportsSearchForm(AdvancedSearchForm):
    search_weight = forms.TypedMultipleChoiceField(label=_("Report Types"),
                                                   help_text=_("Limit search to certain report types."),
                                                   choices=(
                                                            (2, _("Open")),
                                                            (1, _("Resolved")),
                                                            (0, _("Bogus")),
                                                           ),
                                                   coerce=int,
                                                   widget=forms.CheckboxSelectMultiple,
                                                   required=False)