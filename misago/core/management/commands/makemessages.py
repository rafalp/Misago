import codecs
from hashlib import md5
import os
import re

from path import Path

from django.core.management.commands.makemessages import Command as BaseCommand
from django.utils.text import smart_split


I18N_HELPERS = {
    # helper: min valid expression len
    'gettext': 2,
    'ngettext': 4,
    'gettext_noop': 2,
    'pgettext': 3,
    'npgettext': 5
}

HBS_HELPERS = ('unbound', 'if')
HBS_EXPRESSION = re.compile(r'({{{(.*?)}}})|({{(.*?)}})')


class HandlebarsExpression(object):
    def __init__(self, unparsed_expression):
        cleaned_expression = self.clean_expression(unparsed_expression)
        all_helpers = self.parse_expression(
            unparsed_expression, cleaned_expression)

        self.i18n_helpers = self.clean_helpers(all_helpers)

    def get_i18n_helpers(self):
        return self.i18n_helpers

    def clean_expression(self, unparsed):
        cleaned = u''

        for piece in smart_split(unparsed):
            if not cleaned and piece in HBS_HELPERS:
                continue
            if not piece.startswith('=') and not cleaned.endswith('='):
                cleaned += ' '
            cleaned += piece

        return cleaned.strip()

    def parse_expression(self, unparsed, cleaned):
        helper = []
        helpers = [helper]
        stack = [helper]

        for piece in smart_split(cleaned):
            if piece.endswith(')'):
                stack[-1].append(piece.rstrip(')').strip())
                while piece.endswith(')'):
                    piece = piece[:-1].strip()
                    stack.pop()
                continue

            if not piece.startswith(('\'', '"')):
                if piece.startswith('('):
                    piece = piece[1:].strip()
                    if piece.startswith('('):
                        continue
                    else:
                        helper = [piece]
                        helpers.append(helper)
                        stack.append(helper)
                else:
                    is_kwarg = re.match(r'^[_a-zA-Z]+([_a-zA-Z0-9]+?)=', piece)
                    if is_kwarg and not piece.endswith('='):
                        piece = piece[len(is_kwarg.group(0)):]
                        if piece.startswith('('):
                            helper = [piece[1:].strip()]
                            helpers.append(helper)
                            stack.append(helper)
                    else:
                        stack[-1].append(piece)
            else:
                stack[-1].append(piece)

        return helpers

    def clean_helpers(self, all_helpers):
        i18n_helpers = []
        for helper in all_helpers:
            i18n_helper_len = I18N_HELPERS.get(helper[0])
            if i18n_helper_len and len(helper) >= i18n_helper_len:
                i18n_helpers.append(helper[:i18n_helper_len])
        return i18n_helpers


class HandlebarsTemplate(object):
    def __init__(self, content):
        self.expressions = {}
        self.content = content

    def get_converted_content(self):
        stripped_content = self.strip_expressions(self.content)
        stripped_content = self.strip_non_expressions(stripped_content)
        replaced_content = self.replace_expressions(stripped_content)
        return replaced_content

    def strip_expressions(self, content):
        def replace_expression(matchobj):
            trimmed_expression = matchobj.group(0).lstrip('{').rstrip('}')
            parsed_expression = HandlebarsExpression(trimmed_expression)

            expression_i18n_helpers = parsed_expression.get_i18n_helpers()

            if expression_i18n_helpers:
                self.expressions[matchobj.group(0)] = expression_i18n_helpers
                return matchobj.group(0)
            else:
                return ''

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
            js_functions = []
            for helper in self.expressions.get(matchobj.group(0)):
                function, args = helper[0], helper[1:]
                js_functions.append('%s(%s);' % (function, ', '.join(args)))
            return ' '.join(js_functions)

        return HBS_EXPRESSION.sub(replace_expression, content)


class HandlebarsFile(object):
    def __init__(self, hbs_path, make_js_file=True):
        self.hbs_path = hbs_path
        self.path_suffix = self.make_js_path_suffix(hbs_path)
        self.js_path = self.make_js_path(hbs_path, self.path_suffix)

        if make_js_file:
            self.make_js_file(self.hbs_path, self.js_path)

    def make_js_path_suffix(self, hbs_path):
        return '%s.makemessages.js' % md5(hbs_path).hexdigest()[:8]

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
            files.append(HandlebarsFile(hbs_file))
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
