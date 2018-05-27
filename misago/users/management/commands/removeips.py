
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

UserModel = get_user_model()

class Command(BaseCommand):
    help = "Deletes all user registered IPs"

    def handle(self, *args, **options):
      for user in UserModel.objects.all():
        user.joined_from_ip = "0.0.0.0"
        user.save()
      self.stdout.write("Users IP is successfully updated to 0.0.0.0")
