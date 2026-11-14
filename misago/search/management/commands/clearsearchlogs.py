from time import time

from django.core.management.base import BaseCommand, CommandError

from ....conf.shortcuts import get_dynamic_settings
from ...logging import delete_all_search_logs, delete_old_search_logs


class Command(BaseCommand):
    help = "Clears search logs."

    def add_arguments(self, parser):
        parser.add_argument(
            "--all",
            action="store_true",
            dest="delete_all",
            help="Delete all search logs, not just ones older than retention.",
        )
        parser.add_argument(
            "--noinput",
            "--no-input",
            action="store_false",
            dest="interactive",
            help="Do NOT prompt the user for confirmation.",
        )

    def handle(self, *args, **options):
        interactive = options["interactive"]

        if options["delete_all"]:
            self.delete_all(interactive)
        else:
            self.delete_old(interactive)

    def delete_all(self, interactive: bool):
        if interactive:
            message = (
                "This will DELETE ALL search logs!"
                "\n"
                "Are you sure you want to do this?\n\n"
                "Type 'yes' to continue, or 'no' to cancel: "
            )

            if input(message) != "yes":
                raise CommandError("Deleting all search logs cancelled.")

            self.stdout.write("\n")

        start_time = time()
        deleted = delete_all_search_logs()

        self.write_success_message(deleted, start_time)

    def delete_old(self, interactive: bool):
        settings = get_dynamic_settings()
        log_retention = settings.search_log_retention

        if interactive:
            if log_retention == 1:
                message = "This will DELETE search logs older than one day!"
            else:
                message = (
                    f"This will DELETE search logs older than {log_retention} days!"
                )

            message += (
                "\n"
                "Are you sure you want to do this?\n\n"
                "Type 'yes' to continue, or 'no' to cancel: "
            )

            if input(message) != "yes":
                raise CommandError("Deleting old search logs cancelled.")

            self.stdout.write("\n")

        start_time = time()
        deleted = delete_old_search_logs(log_retention)

        self.write_success_message(deleted, start_time)

    def write_success_message(self, deleted: int, start_time: float):
        total_time = "{:.2f}s".format(time() - start_time)

        if deleted == 1:
            self.stdout.write(f"Deleted one search log in {total_time}.")
        else:
            self.stdout.write(f"Deleted {deleted} search logs in {total_time}.")
