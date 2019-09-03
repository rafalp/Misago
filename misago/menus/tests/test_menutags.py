from django.test import TestCase
from django.template import Context, Template


from ..models import MenuLink


class MenuLinksTagsTests(TestCase):
    def test_top_menu_links_output(self):
        MenuLink.objects.create(
            link="https://misago.gitbook.io",
            title="Misago Docs",
            position=MenuLink.POSITION_TOP,
        )
        context = Context()
        template = Template("{% load misago_menutags %}" "{% top_menu_links %}")
        expected = '<li><a href="https://misago.gitbook.io">Misago Docs</a></li>'
        self.assertInHTML(expected, template.render(context))

    def test_footer_menu_links_output(self):
        MenuLink.objects.create(
            link="https://misago.gitbook.io/docs/writingnewadminactions",
            title="Misago Admin Actions",
            position=MenuLink.POSITION_TOP,
        )
        context = Context()
        template = Template("{% load misago_menutags %}" "{% top_menu_links %}")
        expected = '<li><a href="https://misago.gitbook.io/docs/writingnewadminactions">Misago Admin Actions</a></li>'
        self.assertInHTML(expected, template.render(context))
