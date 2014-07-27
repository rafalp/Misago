import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Shows requirements.txt for current Misago version'

    def handle(self, *args, **options):
        #MISAGO_DIR = os.path.join(os.path.dirname(__file__))
        APP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        MISAGO_DIR = os.path.dirname(APP_DIR)
        PROJECT_DIR = os.path.join(MISAGO_DIR, 'project_template')
        REQUIREMENTS_PATH = os.path.join(PROJECT_DIR, 'requirements.txt')

        with open(REQUIREMENTS_PATH, 'r') as resq:
            self.stdout.write(resq.read())
