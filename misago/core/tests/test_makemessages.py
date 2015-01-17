from django.test import TestCase

from misago.core.management.commands.makemessages import (
    HandlebarsExpression, HandlebarsTemplate, HandlebarsFile)


class HandlebarsExpressionTests(TestCase):
    def test_get_i18n_helpers(self):
        """expression parser finds i18n helpers"""
        expression = HandlebarsExpression("some.expression")
        self.assertFalse(expression.get_i18n_helpers())

        expression = HandlebarsExpression("bind-attr src=user.avatar")
        self.assertFalse(expression.get_i18n_helpers())

        expression = HandlebarsExpression("gettext 'misiek'")
        self.assertTrue(expression.get_i18n_helpers())

        expression = HandlebarsExpression("gettext '%(user)s has %(trait)s' user=user.username trait=(gettext user.trait)")
        helpers = expression.get_i18n_helpers()
        self.assertEqual(len(helpers), 2)
        self.assertEqual(helpers[0], ['gettext', "'%(user)s has %(trait)s'"])
        self.assertEqual(helpers[1], ['gettext', "user.trait"])

        expression = HandlebarsExpression('gettext "%(param)s!" param = (gettext "nested once" param = (gettext "nested twice")) otherparam= (gettext "nested once again")')
        helpers = expression.get_i18n_helpers()
        self.assertEqual(len(helpers), 4)
        self.assertEqual(helpers[0], ['gettext', '"%(param)s!"'])
        self.assertEqual(helpers[1], ['gettext', '"nested once"'])
        self.assertEqual(helpers[2], ['gettext', '"nested twice"'])
        self.assertEqual(helpers[3], ['gettext', '"nested once again"'])


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
        VALID_CASES = (
            '%s',
            'unbound %s',
            'something (%s)',
            'unbound something (%s)',
            'if condition (%s)',
            'something "lorem ipsum" some.var kwarg=(%s) otherkwarg=(helper something)'
        )

        for case in VALID_CASES:
            self.subtest("{{%s}}" % case)
            self.subtest("{{ %s }}" % case)
            self.subtest("{{{%s}}}" % case)
            self.subtest("{{{ %s }}}" % case)

    def subtest(self, case_template):
        CASES = (
            (
                "gettext 'Lorem ipsum'",
                "gettext('Lorem ipsum');"
            ),
            (
                "gettext 'Lorem %(vis)s' vis=name",
                "gettext('Lorem %(vis)s');"
            ),
            (
                "gettext 'Lorem %(vis)s' vis=(gettext user.vis)",
                "gettext('Lorem %(vis)s'); gettext(user.vis);"
            ),
            (
                "gettext some_variable",
                "gettext(some_variable);"
            ),
            (
                "gettext 'Lorem ipsum'",
                "gettext('Lorem ipsum');"
            ),
            (
                "gettext 'Lorem %(vis)s' vis=name",
                "gettext('Lorem %(vis)s');"
            ),
            (
                "gettext some_variable",
                "gettext(some_variable);"
            ),
            (
                "gettext some_variable user=user.username",
                "gettext(some_variable);"
            ),
            (
                "ngettext '%(count)s apple' '%(count)s apples' apples_count",
                "ngettext('%(count)s apple', '%(count)s apples', apples_count);"
            ),
            (
                "ngettext '%(user)s has %(count)s apple' '%(user)s has %(count)s apples' apples_count user=user.username",
                "ngettext('%(user)s has %(count)s apple', '%(user)s has %(count)s apples', apples_count);"
            ),
            (
                "ngettext apple apples apples_count",
                "ngettext(apple, apples, apples_count);"
            ),
            (
                "ngettext '%(count)s apple' apples apples_count",
                "ngettext('%(count)s apple', apples, apples_count);"
            ),
            (
                "ngettext '%(user)s has %(count)s apple' apples apples_count user=user.username",
                "ngettext('%(user)s has %(count)s apple', apples, apples_count);"
            ),
            (
                "gettext_noop 'Lorem ipsum'",
                "gettext_noop('Lorem ipsum');"
            ),
            (
                "gettext_noop 'Lorem %(vis)s' vis=name",
                "gettext_noop('Lorem %(vis)s');"
            ),
            (
                "gettext_noop some_variable",
                "gettext_noop(some_variable);"
            ),
            (
                "gettext_noop 'Lorem ipsum'",
                "gettext_noop('Lorem ipsum');"
            ),
            (
                "gettext_noop 'Lorem %(vis)s' vis=name",
                "gettext_noop('Lorem %(vis)s');"
            ),
            (
                "gettext_noop some_variable",
                "gettext_noop(some_variable);"
            ),
            (
                "pgettext 'month' 'may'",
                "pgettext('month', 'may');"
            ),
            (
                "pgettext 'month' month_name",
                "pgettext('month', month_name);"
            ),
            (
                "pgettext 'day of month' 'May, %(day)s' day=calendar.day",
                "pgettext('day of month', 'May, %(day)s');"
            ),
            (
                "pgettext context value day=calendar.day",
                "pgettext(context, value);"
            ),
            (
                "npgettext 'fruits' '%(count)s apple' '%(count)s apples' apples_count",
                "npgettext('fruits', '%(count)s apple', '%(count)s apples', apples_count);"
            ),
            (
                "npgettext 'fruits' '%(user)s has %(count)s apple' '%(user)s has %(count)s apples' apples_count user=user.username",
                "npgettext('fruits', '%(user)s has %(count)s apple', '%(user)s has %(count)s apples', apples_count);"
            ),
            (
                "npgettext context apple apples apples_count",
                "npgettext(context, apple, apples, apples_count);"
            ),
            (
                "npgettext context '%(count)s apple' apples apples_count",
                "npgettext(context, '%(count)s apple', apples, apples_count);"
            ),
            (
                "npgettext 'fruits' '%(user)s has %(count)s apple' apples apples_count user=user.username",
                "npgettext('fruits', '%(user)s has %(count)s apple', apples, apples_count);"
            ),
        )

        assertion_msg = """
HBS template was parsed incorrectly:

input:      %s
output:     %s
expected:   %s
"""

        for test, expected_output in CASES:
            test_input = case_template % test

            template = HandlebarsTemplate(case_template % test)
            test_output = template.get_converted_content()

            self.assertEqual(
                test_output, expected_output,
                assertion_msg % (test_input, test_output, expected_output))

    def test_multiple_expressions(self):
        """multiple expressions are handled"""
        template = HandlebarsTemplate("{{gettext 'Posted by:'}} <strong>{{gettext user.rank.title}}</strong>; <em>{{ user.city }}</em>")
        self.assertEqual(template.get_converted_content(),
                         "gettext('Posted by:');gettext(user.rank.title);")

        template = HandlebarsTemplate("""{{gettext 'Posted by:'}}<br>
                                         {{gettext user.rank.title}}""")
        self.assertEqual(template.get_converted_content(),
                         "gettext('Posted by:');\ngettext(user.rank.title);")

        template = HandlebarsTemplate("""<h1>{{ thread.title }}</h1>
            {{gettext 'Posted by:'}}<br>

            {{gettext user.rank.title}}""")
        self.assertEqual(template.get_converted_content(),
                         "\ngettext('Posted by:');\n\ngettext(user.rank.title);")


class HandlebarsFileTests(TestCase):
    def test_make_js_path(self):
        """Object correctly translates hbs path to temp js path"""
        hbs_path = "templates/application.hbs"
        test_file = HandlebarsFile(hbs_path, False)

        suffix = test_file.make_js_path_suffix(hbs_path)
        self.assertTrue(suffix.endswith(".makemessages.js"))

        js_path = test_file.make_js_path(hbs_path, suffix)
        self.assertTrue(js_path.startswith(hbs_path))
        self.assertTrue(js_path.endswith(suffix))
