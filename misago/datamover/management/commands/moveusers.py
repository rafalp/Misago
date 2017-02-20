from misago.datamover import avatars, bans, users
from misago.datamover.management.base import BaseCommand


class Command(BaseCommand):
    help = ("Moves users, avatars, followers, blocks and bans from Misago 0.5")

    def handle(self, *args, **options):
        self.stdout.write("Moving users from Misago 0.5:")

        self.start_timer()
        users.move_users(self.stdout, self.style)
        self.stdout.write(self.style.SUCCESS("Moved users in %s" % self.stop_timer()))

        self.start_timer()
        avatars.move_avatars(self.stdout, self.style)
        self.stdout.write(self.style.SUCCESS("Moved avatars in %s" % self.stop_timer()))

        self.start_timer()
        users.move_followers()
        self.stdout.write(self.style.SUCCESS("Moved followers in %s" % self.stop_timer()))

        self.start_timer()
        users.move_blocks()
        self.stdout.write(self.style.SUCCESS("Moved blocks in %s" % self.stop_timer()))

        self.start_timer()
        users.move_namehistory()
        self.stdout.write(self.style.SUCCESS("Moved name history in %s" % self.stop_timer()))

        self.start_timer()
        bans.move_bans()
        self.stdout.write(self.style.SUCCESS("Moved bans in %s" % self.stop_timer()))
