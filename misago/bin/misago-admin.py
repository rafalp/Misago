"""
Misago wrapper for Django admin

This wrapper users Misago makemessages instead of Django one, making it work
for Handlebars templates in addition to .js files.
"""
from django.core.management import ManagementUtility

from misago.core.management.commands.makemessages import Command


class MisagoAdmin(ManagementUtility):
    def fetch_command(self, subcommand):
        if subcommand == "makemessages":
            return Command()
        else:
            return super(MisagoAdmin, self).fetch_command(subcommand)


if __name__ == '__main__':
    utility = MisagoAdmin()
    utility.execute()
