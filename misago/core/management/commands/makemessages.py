import codecs
from hashlib import md5
import os
import re

from path import Path

from django.core.management.commands.makemessages import Command as BaseCommand
from django.utils.text import smart_split


HBS_EXPRESSION = re.compile(r'({{{(.*?)}}})|({{(.*?)}})')

HELPERS = {
    'gettext': 1,
    'ngettext': 3,
    'gettext_noop': 1,
    'pgettext': 2,
    'npgettext': 4
}


class HandlebarsTemplate(object):
    def __init__(self, content):
        self.content = content

    def get_converted_content(self):
        stripped_content = self.strip_expressions(self.content)
        stripped_content = self.strip_non_expressions(stripped_content)
        replaced_content = self.replace_expressions(stripped_content)
        return replaced_content

    def strip_expressions(self, content):
        def replace_expression(matchobj):
            trimmed_expression = matchobj.group(0).lstrip('{').rstrip('}')
            trimmed_expression = trimmed_expression.strip()

            expression_words = trimmed_expression.split()
            if expression_words[0] in HELPERS:
                return matchobj.group(0)
            else:
                return ' ' * len(matchobj.group(0))

        return HBS_EXPRESSION.sub(replace_expression, self.content)

    def strip_non_expressions(self, content):
        stripped = u''

        cursor = 0
        for expression in HBS_EXPRESSION.finditer(content):
            position = content.find(expression.group(0), cursor)

            content_slice = content[cursor:position]
            if content_slice:
                slice_lines = len(content_slice.splitlines())
                if slice_lines:
                    stripped += '\n' * (slice_lines - 1)

            stripped += expression.group(0)
            cursor = position + len(expression.group(0))

        return stripped

    def replace_expressions(self, content):
        def replace_expression(matchobj):
            trimmed_expression = matchobj.group(0).lstrip('{').rstrip('}')
            trimmed_expression = trimmed_expression.strip()

            expression_bits = [b for b in smart_split(trimmed_expression)]
            function = expression_bits[0]
            args = expression_bits[1:HELPERS[function] + 1]
            return '%s(%s);' % (function, ', '.join(args))
        return HBS_EXPRESSION.sub(replace_expression, content)


class HandlebasFile(object):
    def __init__(self, hbs_path):
        self.hbs_path = hbs_path
        self.path_suffix = self.make_js_path_suffix(hbs_path)
        self.js_path = self.make_js_path(hbs_path, self.path_suffix)

        self.make_js_file(self.hbs_path, self.js_path)

    def make_js_path_suffix(self, hbs_path):
        return '%s.tmp.js' % md5(hbs_path).hexdigest()[:8]

    def make_js_path(self, hbs_path, path_suffix):
        return Path('%s.%s' % (unicode(hbs_path), path_suffix))

    def make_js_file(self, hbs_path, js_path):
        file_content = u''
        with codecs.open(hbs_path, encoding='utf-8', mode="r") as hbs_file:
            file_content = hbs_file.read()

        js_file = codecs.open(js_path, encoding='utf-8', mode='w')
        js_file.write(HandlebarsTemplate(file_content).get_converted_content())
        js_file.close()

    def delete(self):
        if self.js_path.exists() and self.js_path.isfile():
            self.js_path.unlink()


class Command(BaseCommand):
    help = ("Runs over the entire source tree of the current directory and "
"pulls out all strings marked for translation. It creates (or updates) a message "
"file in the conf/locale (in the django tree) or locale (for projects and "
"applications) directory.\n\nIf command is executed for JavaScript files, it "
"also pulls strings from Misago Handlebars.js files.\n\nYou must run this "
"command with one of either the --locale, --exclude or --all options.")

    JS_TEMPLATES = ('.hbs', '.handlebars')

    def handle(self, *args, **options):
        locales = options.get('locale')
        self.domain = options.get('domain')

        subdirs = [unicode(d.basename()) for d in Path(os.getcwd()).dirs()]
        use_subroutines = 'locale' in subdirs and self.domain == 'djangojs'

        tmp_js_files = []
        if use_subroutines:
            # fake js files from templates
            tmp_js_files = self.prepare_tmp_js_files();

        super(Command, self).handle(*args, **options)

        if use_subroutines:
            # cleanup everything
            self.cleanup_tmp_js_templates(tmp_js_files);
            self.cleanup_po_files(locales, tmp_js_files);

    def prepare_tmp_js_files(self):
        files = []
        for hbs_file in Path(os.getcwd()).walkfiles('*.hbs'):
            files.append(HandlebasFile(hbs_file))
        return files

    def cleanup_po_files(self, locales, tmp_js_files):
        strip_tokens = [js_file.path_suffix for js_file in tmp_js_files]

        for po_file in Path(os.getcwd()).walkfiles('djangojs.po'):
            if not locales or po_file.splitall()[-3] in locales:
                self.cleanup_po_file(po_file, strip_tokens)

    def cleanup_po_file(self, po_path, strip_tokens):
        file_content = u''
        with codecs.open(po_path, encoding='utf-8', mode="r") as po_file:
            file_content = po_file.read()

        for token in strip_tokens:
            file_content = file_content.replace(token, '')

        po_file = codecs.open(po_path, encoding='utf-8', mode='w')
        po_file.write(file_content)
        po_file.close()

    def cleanup_tmp_js_templates(self, tmp_js_files):
        for js_file in tmp_js_files:
            js_file.delete()
