from django.template import Context, Template
from django.test import TestCase, override_settings

from ..templatetags.misago_absoluteurl import absoluteurl
from ..templatetags.misago_batch import batch, batchnonefilled

TEST_ADDRESS = "https://testsite.com/"


class AbsoluteUrlTests(TestCase):
    @override_settings(MISAGO_ADDRESS=None)
    def test_address_is_none(self):
        """template tag returns null if address setting is not filled"""
        result = absoluteurl("misago:index")
        self.assertIsNone(result)

    @override_settings(MISAGO_ADDRESS=TEST_ADDRESS)
    def test_prefix_url(self):
        """template tag prefixes already reversed url"""
        result = absoluteurl("/")
        self.assertEqual(result, TEST_ADDRESS)

    @override_settings(MISAGO_ADDRESS=TEST_ADDRESS)
    def test_prefix_url_name(self):
        """template tag reverses url name and prefixes it"""
        result = absoluteurl("misago:index")
        self.assertEqual(result, TEST_ADDRESS)

    @override_settings(MISAGO_ADDRESS=TEST_ADDRESS)
    def test_dont_change_absolute_url(self):
        """template tag doesn't change already absolute urls"""
        absolute_url = "https://github.com/rafalp/Misago/issues/1067"
        result = absoluteurl(absolute_url)
        self.assertEqual(result, absolute_url)


class CaptureTests(TestCase):
    def setUp(self):
        self.context = Context({"unsafe_name": "The<hr>Html"})

    def test_capture(self):
        """capture content to variable"""
        tpl_content = """
{% load misago_capture %}

{% capture as the_var %}
{{ unsafe_name }}
{% endcapture %}
Hello, <b>{{ the_var|safe }}</b>
"""

        tpl = Template(tpl_content)
        render = tpl.render(self.context).strip()
        self.assertIn("The&lt;hr&gt;Html", render)
        self.assertNotIn("<b>The&lt;hr&gt;Html</b>", render)

    def test_capture_trimmed(self):
        """capture trimmed content to variable"""
        tpl_content = """
{% load misago_capture %}

{% capture trimmed as the_var %}
{{ unsafe_name }}
{% endcapture %}
Hello, <b>{{ the_var|safe }}</b>
"""

        tpl = Template(tpl_content)
        render = tpl.render(self.context).strip()
        self.assertIn("<b>The&lt;hr&gt;Html</b>", render)


class BatchTests(TestCase):
    def test_batch(self):
        """standard batch yields valid results"""
        batch = "loremipsum"
        yields = [["l", "o", "r"], ["e", "m", "i"], ["p", "s", "u"], ["m"]]

        for i, test_yield in enumerate(batch(batch, 3)):
            self.assertEqual(test_yield, yields[i])

    def test_batchnonefilled(self):
        """none-filled batch yields valid results"""
        batch = "loremipsum"
        yields = [["l", "o", "r"], ["e", "m", "i"], ["p", "s", "u"], ["m", None, None]]

        for i, test_yield in enumerate(batchnonefilled(batch, 3)):
            self.assertEqual(test_yield, yields[i])


class MockUser(object):
    id = 12
    pk = 12
    username = "User"
    slug = "user"


class ShorthandsTests(TestCase):
    def test_iftrue_for_true(self):
        """iftrue renders value for true"""
        tpl_content = """
{% load misago_shorthands %}

{{ value|iftrue:result }}
"""

        tpl = Template(tpl_content)
        self.assertEqual(
            tpl.render(Context({"result": "Ok!", "value": True})).strip(), "Ok!"
        )

    def test_iftrue_for_false(self):
        """iftrue isnt rendering value for false"""
        tpl_content = """
{% load misago_shorthands %}

{{ value|iftrue:result }}
"""

        tpl = Template(tpl_content)
        self.assertEqual(
            tpl.render(Context({"result": "Ok!", "value": False})).strip(), ""
        )

    def test_iffalse_for_true(self):
        """iffalse isnt rendering value for true"""
        tpl_content = """
{% load misago_shorthands %}

{{ value|iffalse:result }}
"""

        tpl = Template(tpl_content)
        self.assertEqual(
            tpl.render(Context({"result": "Ok!", "value": True})).strip(), ""
        )

    def test_iffalse_for_false(self):
        """iffalse renders value for false"""
        tpl_content = """
{% load misago_shorthands %}

{{ value|iffalse:result }}
"""

        tpl = Template(tpl_content)
        self.assertEqual(
            tpl.render(Context({"result": "Ok!", "value": False})).strip(), "Ok!"
        )


class JSONTests(TestCase):
    def test_json_filter(self):
        """as_json filter renders dict as safe json"""
        tpl_content = """
{% load misago_json %}

{{ value|as_json }}
"""

        tpl = Template(tpl_content)
        self.assertEqual(
            tpl.render(Context({"value": {"he</script>llo": 'bo"b!'}})).strip(),
            r'{"he\u003C/script>llo": "bo\"b!"}',
        )


class PageTitleTests(TestCase):
    def test_single_title(self):
        """tag passes trough single title"""
        tpl_content = """
        {% load misago_pagetitle %}

        {% pagetitle item %}
        """

        tpl = Template(tpl_content)
        self.assertEqual(
            tpl.render(Context({"item": "Lorem Ipsum"})).strip(), "Lorem Ipsum"
        )

    def test_parent_title(self):
        """tag builds full title from title and parent name"""
        tpl_content = """
        {% load misago_pagetitle %}

        {% pagetitle item parent=parent %}
        """

        tpl = Template(tpl_content)
        self.assertEqual(
            tpl.render(
                Context({"item": "Lorem Ipsum", "parent": "Some Thread"})
            ).strip(),
            "Lorem Ipsum | Some Thread",
        )

    def test_paged_title(self):
        """tag builds full title from title and page number"""
        tpl_content = """
        {% load misago_pagetitle %}

        {% pagetitle item page=3 %}
        """

        tpl = Template(tpl_content)
        self.assertEqual(
            tpl.render(Context({"item": "Lorem Ipsum"})).strip(),
            "Lorem Ipsum (page: 3)",
        )

    def test_kitchensink_title(self):
        """tag builds full title from all options"""
        tpl_content = """
        {% load misago_pagetitle %}

        {% pagetitle item page=3 parent=parent %}
        """

        tpl = Template(tpl_content)
        self.assertEqual(
            tpl.render(
                Context({"item": "Lorem Ipsum", "parent": "Some Thread"})
            ).strip(),
            "Lorem Ipsum (page: 3) | Some Thread",
        )
