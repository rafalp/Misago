from django.core.management.commands.makemessages import Command as BaseCommand


class Command(BaseCommand):
    help = ("Runs over the entire source tree of the current directory and "
"pulls out all strings marked for translation. It creates (or updates) a message "
"file in the conf/locale (in the django tree) or locale (for projects and "
"applications) directory.\n\nIf command is executed for JavaScript files, it "
"also pulls strings from Misago Handlebars.js files.\n\nYou must run this "
"command with one of either the --locale, --exclude or --all options.")

    JS_TEMPLATES = ('.hbs', '.handlebars')

    def handle(self, *args, **options):
        locale = options.get('locale')
        exclude = options.get('exclude')
        self.domain = options.get('domain')
        self.verbosity = options.get('verbosity')
        process_all = options.get('all')
        extensions = options.get('extensions')
        self.symlinks = options.get('symlinks')

        if self.domain == 'djangojs':
            # fake js files from templates
            self.prepare_tmp_js_templates();

        super(Command, self).handle(*args, **options)

        if self.domain == 'djangojs':
            # cleanup everything
            self.cleanup_po_files();
            self.cleanup_tmp_js_templates();

    def prepare_tmp_js_templates(self):
        pass

    def cleanup_po_files(self):
        pass

    def cleanup_tmp_js_templates(self):
        pass
