from django.contrib.auth import get_user_model
from django.template import Context, Template
from django.test import TestCase


class TemplateTagsTests(TestCase):
    def test_user_avatar_filter(self):
        """avatar filter returns url to avatar image"""
        User = get_user_model()
        user = User.objects.create_user('Bob', 'bob@test.com', 'pass123')

        tpl_content = """
{% load misago_avatars %}

{{ user|avatar }}
{{ user|avatar:100 }}
{{ user.pk|avatar }}
{{ user.pk|avatar:100 }}
"""

        tpl = Template(tpl_content)
        render = tpl.render(Context({'user': user})).strip().splitlines()

        pk = user.pk

        self.assertEqual(render[0].strip(), '/user-avatar/200/%s.png' % pk)
        self.assertEqual(render[1].strip(), '/user-avatar/100/%s.png' % pk)
        self.assertEqual(render[2].strip(), '/user-avatar/200/%s.png' % pk)
        self.assertEqual(render[3].strip(), '/user-avatar/100/%s.png' % pk)

    def test_blankavatar_tag(self):
        """{% blankavatar %} tag returns url to default image"""
        tpl_content = """
{% load misago_avatars %}

{% blankavatar %}
{% blankavatar 100 %}
"""

        tpl = Template(tpl_content)
        render = tpl.render(Context()).strip().splitlines()

        self.assertEqual(render[0].strip(), '/user-avatar/200.png')
        self.assertEqual(render[1].strip(), '/user-avatar/100.png')
