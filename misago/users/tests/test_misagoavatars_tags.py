from django.contrib.auth import get_user_model
from django.template import Context, Template
from django.test import TestCase


UserModel = get_user_model()


class TemplateTagsTests(TestCase):
    def test_user_avatar_filter(self):
        """avatar filter returns url to avatar image"""
        user = UserModel.objects.create_user('Bob', 'bob@test.com', 'pass123')

        user.avatars = [
            {
                'size': 400,
                'url': '/avatar/400.png'
            },
            {
                'size': 128,
                'url': '/avatar/400.png'
            },
            {
                'size': 30,
                'url': '/avatar/30.png'
            },
        ]

        tpl_content = """
{% load misago_avatars %}

{{ user|avatar }}
{{ user|avatar:100 }}
{{ user|avatar:30 }}
{{ user|avatar:10 }}
"""

        tpl = Template(tpl_content)
        render = tpl.render(Context({'user': user})).strip().splitlines()

        self.assertEqual(render[0].strip(), user.avatars[0]['url'])
        self.assertEqual(render[1].strip(), user.avatars[1]['url'])
        self.assertEqual(render[2].strip(), user.avatars[2]['url'])
        self.assertEqual(render[3].strip(), user.avatars[2]['url'])
