from django.core.urlresolvers import reverse as django_reverse
from django.utils.translation import ugettext as _
from misago.admin import site
from misago.admin.widgets import *
from misago.utils import slugify
from misago.security.admin.qatest.forms import QATestForm
from misago.security.models import QATest

def reverse(route, target=None):
    if target:
        return django_reverse(route, kwargs={'target': target.pk, 'slug': slugify(target.question)})
    return django_reverse(route)

"""
Views
"""
class List(ListWidget):
    """
    List QA Tests
    """
    admin = site.get_action('qa')
    id = 'list'
    columns=(
             ('question', _("Question"), 50),
             ('helptext', _("Help")),
             )
    default_sorting = 'question'
    sortables={
               'question': 1,
               'helptext': 1,
              }
    filters = ['question', 'helptext']
    filters_layout = []
    empty_message = _('No Question and Answer tests have been found. Change search criteria and try again.')
    nothing_checked_message = _('You have to check at least one test.')
    actions=(
             ('delete', _("Delete selected"), _("Are you sure you want to delete selected questions?")),
             )
    
    def get_item_actions(self, request, item):
        return (
                self.action('pencil', _("Edit Test"), reverse('admin_qa_edit', item)),
                self.action('remove', _("Delete Test"), reverse('admin_qa_delete', item), post=True, prompt=_("Are you sure you want to delete this test?")),
                )

    def action_delete(self, request, items, checked):
        QATest.objects.filter(id__in=checked).delete()
        return BasicMessage(_('Selected Q&A Tests have been deleted successfully.'), 'success'), reverse('admin_qa')
    

class New(FormWidget):
    """
    Create New QA Test
    """
    admin = site.get_action('qa')
    id = 'new'
    fallback = 'admin_qa' 
    form = QATestForm
    submit_button = _("Save Test")
        
    def get_new_url(self, request, model):
        return reverse('admin_qa_new')
    
    def get_edit_url(self, request, model):
        return reverse('admin_qa_edit', model)
    
    def submit_form(self, request, form, target):
        new_test = QATest(
                          question=form.cleaned_data['question'],
                          helptext=form.cleaned_data['helptext'],
                          answers=form.cleaned_data['answers'],
                          )
        new_test.save(force_insert=True)
        return new_test, BasicMessage(_('New Q&A Test "%(name)s" has been saved.' % {'name': form.cleaned_data['question']}), 'success')
    
   
class Edit(FormWidget):
    """
    Edit QA Test
    """
    admin = site.get_action('qa')
    id = 'edit'
    name = _("Edit QA Test")
    fallback = 'admin_qa'
    form = QATestForm
    target_name = 'question'
    notfound_message = _('Requested Question and Answer test could not be found.')
    submit_fallback = True
    
    def get_url(self, request, model):
        return reverse('admin_qa_edit', model)
    
    def get_edit_url(self, request, model):
        return self.get_url(request, model)
    
    def get_initial_data(self, request, model):
        return {
                'question': model.question,
                'helptext': model.helptext,
                'answers': model.answers,
                }
    
    def submit_form(self, request, form, target):
        old_question = target.question
        target.question = form.cleaned_data['question']
        target.helptext = form.cleaned_data['helptext']
        target.answers = form.cleaned_data['answers']
        target.save(force_update=True)
        return target, BasicMessage(_('Changes in Q&A Test "%(name)s" have been saved.' % {'name': old_question}), 'success')


class Delete(ButtonWidget):
    """
    Delete QA Test
    """
    admin = site.get_action('qa')
    id = 'delete'
    fallback = 'admin_qa'
    notfound_message = _('Requested Question and Answer test could not be found.')
    
    def action(self, request, target):
        target.delete()
        return BasicMessage(_('Q&A Test "%(name)s" has been deleted.' % {'name': target.question}), 'success'), False
        