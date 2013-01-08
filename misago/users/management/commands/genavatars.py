from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from path import path
try:
    from PIL import Image
    has_pil = True
except ImportError:
    has_pil = False
from misago.users.models import User
from misago.utils.avatars import resizeimage

class Command(BaseCommand):
    help = 'Regenerates avatar images for new dimensions'
    def handle(self, *args, **options):
        if not has_pil:
            raise CommandError('genavatars requires Python Imaging Library to be installed in order to run')
        self.scale_user_avatars()
        self.scale_gallery_avatars()
        self.stdout.write('\n\nAvatar images have been regenerated.\n')

    def scale_image(self, image_src, image_dir=None):
        image_name = path.basename(path(image_src))
        if not image_dir:
            image_dir = path.dirname(path(image_src)) + '/%s_'
        for size in settings.AVATAR_SIZES[1:]:
            resizeimage(image_src, size, image_dir % size + image_name)

    def scale_user_avatars(self):
        for user in User.objects.filter(avatar_type='upload').iterator():
            for image in path(settings.MEDIA_ROOT).joinpath('avatars').files('*_%s' % user.avatar_image):
                if not image.isdir():
                    image.remove()
            self.scale_image(settings.MEDIA_ROOT + 'avatars/' + user.avatar_image)

    def scale_gallery_avatars(self):
        try:
            thumb_dir = path(settings.STATICFILES_DIRS[0]).joinpath('avatars').joinpath('_thumbs')
            items = [thumb_dir]
            for item in thumb_dir.walk():
                items.append(item)
            for item in reversed(items):
                if item.isdir():
                    item.rmdir()
                else:
                    item.remove()
        except Exception:
            pass
        avatars_dir = path(settings.STATICFILES_DIRS[0]).joinpath('avatars')
        avatars_len = len(avatars_dir)
        avatars_list = []
        for directory in avatars_dir.dirs():
            avatars_list += directory.files('*.gif')
            avatars_list += directory.files('*.jpg')
            avatars_list += directory.files('*.jpeg')
            avatars_list += directory.files('*.png')
        thumb_dir = path(settings.STATICFILES_DIRS[0]).joinpath('avatars').joinpath('_thumbs')
        thumb_dir.mkdir(777)
        for size in settings.AVATAR_SIZES[1:]:
            thumb_dir.joinpath(str(size)).mkdir(777)
        for directory in avatars_dir.dirs():
            dirname = path(directory[avatars_len:]).basename()
            if dirname != '_thumbs':
                for size in settings.AVATAR_SIZES[1:]:
                    thumb_dir.joinpath(str(size)).joinpath(dirname).mkdir(777)
        for avatar in avatars_list:
            self.scale_image(avatar,
                             thumb_dir + '/%s' + avatar.dirname()[avatars_len:] + '/')
