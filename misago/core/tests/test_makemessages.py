from django.test import TestCase

from misago.core.management.commands.makemessages import (HandlebarsTemplate,
                                                          HandlebarsFile)


class HandlebarsFileTests(TestCase):
    def test_make_js_path(self):
        """Object correctly translates hbs path to temp js path"""
        hbs_path = "templates/application.hbs"
        test_file = HandlebarsFile(hbs_path, False)

        suffix = test_file.make_js_path_suffix(hbs_path)
        self.assertTrue(suffix.endswith(".tmp.js"))

        js_path = test_file.make_js_path(hbs_path, suffix)
        self.assertTrue(js_path.startswith(hbs_path))
        self.assertTrue(js_path.endswith(suffix))


class HandlebarsTemplateTests(TestCase):
    def test_empty_file(self):
        """empty file causes no errors"""
        template = HandlebarsTemplate("")
        self.assertEqual(template.get_converted_content(), "")

    def test_stripped_expression(self):
        """non-i18n expression is stripped"""
        template = HandlebarsTemplate("{{ some.expression }}")
        self.assertEqual(template.get_converted_content(), "")

    def test_invalid_expression_stripping(self):
        """invalid i18n expressions are stripped"""
        template = HandlebarsTemplate("{{gettext }}")
        self.assertEqual(template.get_converted_content(), "")

        template = HandlebarsTemplate("{{ngettext }}")
        self.assertEqual(template.get_converted_content(), "")

        template = HandlebarsTemplate("{{ngettext 'apple' }}")
        self.assertEqual(template.get_converted_content(), "")

        template = HandlebarsTemplate("{{ngettext 'apple' 'apples' }}")
        self.assertEqual(template.get_converted_content(), "")

        template = HandlebarsTemplate("{{gettext_noop }}")
        self.assertEqual(template.get_converted_content(), "")

        template = HandlebarsTemplate("{{pgettext }}")
        self.assertEqual(template.get_converted_content(), "")

        template = HandlebarsTemplate("{{pgettext 'apple' }}")
        self.assertEqual(template.get_converted_content(), "")

        template = HandlebarsTemplate("{{npgettext 'fruit' 'apple' }}")
        self.assertEqual(template.get_converted_content(), "")

    def test_valid_expression_replace(self):
        """valid i18n expressions are replaced"""
        template = HandlebarsTemplate("{{gettext 'Lorem ipsum'}}")
        self.assertEqual(template.get_converted_content(),
                         "gettext('Lorem ipsum');")

        template = HandlebarsTemplate("{{gettext 'Lorem %(vis)s' vis=name}}")
        self.assertEqual(template.get_converted_content(),
                         "gettext('Lorem %(vis)s');")

        template = HandlebarsTemplate("{{gettext some_variable}}")
        self.assertEqual(template.get_converted_content(),
                         "gettext(some_variable);")

        template = HandlebarsTemplate("{{gettext 'Lorem ipsum'}}")
        self.assertEqual(template.get_converted_content(),
                         "gettext('Lorem ipsum');")

        template = HandlebarsTemplate("{{gettext 'Lorem %(vis)s' vis=name}}")
        self.assertEqual(template.get_converted_content(),
                         "gettext('Lorem %(vis)s');")

        template = HandlebarsTemplate("{{gettext some_variable}}")
        self.assertEqual(template.get_converted_content(),
                         "gettext(some_variable);")

        template = HandlebarsTemplate("{{gettext some_variable user=user.username}}")
        self.assertEqual(template.get_converted_content(),
                         "gettext(some_variable);")

        template = HandlebarsTemplate("{{ngettext '%(count)s apple' '%(count)s apples' apples_count}}")
        self.assertEqual(template.get_converted_content(),
                         "ngettext('%(count)s apple', '%(count)s apples', apples_count);")

        template = HandlebarsTemplate("{{ngettext '%(user)s has %(count)s apple' '%(user)s has %(count)s apples' apples_count user=user.username}}")
        self.assertEqual(template.get_converted_content(),
                         "ngettext('%(user)s has %(count)s apple', '%(user)s has %(count)s apples', apples_count);")

        template = HandlebarsTemplate("{{ngettext apple apples apples_count}}")
        self.assertEqual(template.get_converted_content(),
                         "ngettext(apple, apples, apples_count);")

        template = HandlebarsTemplate("{{ngettext '%(count)s apple' apples apples_count}}")
        self.assertEqual(template.get_converted_content(),
                         "ngettext('%(count)s apple', apples, apples_count);")

        template = HandlebarsTemplate("{{ngettext '%(user)s has %(count)s apple' apples apples_count user=user.username}}")
        self.assertEqual(template.get_converted_content(),
                         "ngettext('%(user)s has %(count)s apple', apples, apples_count);")

        template = HandlebarsTemplate("{{gettext_noop 'Lorem ipsum'}}")
        self.assertEqual(template.get_converted_content(),
                         "gettext_noop('Lorem ipsum');")

        template = HandlebarsTemplate("{{gettext_noop 'Lorem %(vis)s' vis=name}}")
        self.assertEqual(template.get_converted_content(),
                         "gettext_noop('Lorem %(vis)s');")

        template = HandlebarsTemplate("{{gettext_noop some_variable}}")
        self.assertEqual(template.get_converted_content(),
                         "gettext_noop(some_variable);")

        template = HandlebarsTemplate("{{gettext_noop 'Lorem ipsum'}}")
        self.assertEqual(template.get_converted_content(),
                         "gettext_noop('Lorem ipsum');")

        template = HandlebarsTemplate("{{gettext_noop 'Lorem %(vis)s' vis=name}}")
        self.assertEqual(template.get_converted_content(),
                         "gettext_noop('Lorem %(vis)s');")

        template = HandlebarsTemplate("{{gettext_noop some_variable}}")
        self.assertEqual(template.get_converted_content(),
                         "gettext_noop(some_variable);")

        template = HandlebarsTemplate("{{pgettext 'month' 'may'}}")
        self.assertEqual(template.get_converted_content(),
                         "pgettext('month', 'may');")

        template = HandlebarsTemplate("{{pgettext 'month' month_name}}")
        self.assertEqual(template.get_converted_content(),
                         "pgettext('month', month_name);")

        template = HandlebarsTemplate("{{pgettext 'day of month' 'May, %(day)s' day=calendar.day}}")
        self.assertEqual(template.get_converted_content(),
                         "pgettext('day of month', 'May, %(day)s');")

        template = HandlebarsTemplate("{{pgettext context value day=calendar.day}}")
        self.assertEqual(template.get_converted_content(),
                         "pgettext(context, value);")

        template = HandlebarsTemplate("{{npgettext 'fruits' '%(count)s apple' '%(count)s apples' apples_count}}")
        self.assertEqual(template.get_converted_content(),
                         "npgettext('fruits', '%(count)s apple', '%(count)s apples', apples_count);")

        template = HandlebarsTemplate("{{npgettext 'fruits' '%(user)s has %(count)s apple' '%(user)s has %(count)s apples' apples_count user=user.username}}")
        self.assertEqual(template.get_converted_content(),
                         "npgettext('fruits', '%(user)s has %(count)s apple', '%(user)s has %(count)s apples', apples_count);")

        template = HandlebarsTemplate("{{npgettext context apple apples apples_count}}")
        self.assertEqual(template.get_converted_content(),
                         "npgettext(context, apple, apples, apples_count);")

        template = HandlebarsTemplate("{{npgettext context '%(count)s apple' apples apples_count}}")
        self.assertEqual(template.get_converted_content(),
                         "npgettext(context, '%(count)s apple', apples, apples_count);")

        template = HandlebarsTemplate("{{npgettext 'fruits' '%(user)s has %(count)s apple' apples apples_count user=user.username}}")
        self.assertEqual(template.get_converted_content(),
                         "npgettext('fruits', '%(user)s has %(count)s apple', apples, apples_count);")

    def test_multiple_expressions(self):
        """multiple expressions are handled"""
        template = HandlebarsTemplate("{{gettext 'Posted by:'}} <strong>{{gettext user.rank.title}}</strong>; <em>{{ user.city }}</em>")
        self.assertEqual(template.get_converted_content(),
                         "gettext('Posted by:');gettext(user.rank.title);")

        template = HandlebarsTemplate("""{{gettext 'Posted by:'}}<br>
                                         {{gettext user.rank.title}}""")
        self.assertEqual(template.get_converted_content(),
                         "gettext('Posted by:');\ngettext(user.rank.title);")
