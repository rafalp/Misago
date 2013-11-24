from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _
from floppyforms import ValidationError
from misago.thread import local

_thread_local = local()

class AttachmentTypeManager(models.Manager):
    def flush_cache(self):
        cache.delete('attachment_types')

    def make_cache(self):
        attachment_types = cache.get('attachment_types', 'nada')
        if attachment_types == 'nada':
            attachment_types = []
            for attachment_type in AttachmentType.objects.order_by('name').iterator():
                attachment_type.roles_pks = [r.pk for r in attachment_type.roles.iterator()]
                attachment_types.append(attachment_type)
            cache.set('attachment_types', attachment_types, None)
        result_dict = {}
        for attachment_type in attachment_types:
            result_dict[attachment_type.pk] = attachment_type
        return result_dict

    def all_types(self):
        try:
            return _thread_local.misago_attachment_types
        except AttributeError:
            _thread_local.misago_attachment_types = self.make_cache()
        return _thread_local.misago_attachment_types

    def find_type(self, filename):
        for attachment_type in self.all_types().values():
            if attachment_type.file_of_type(filename):
                return attachment_type
        return None


class AttachmentType(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    extensions = models.CharField(max_length=255)
    size_limit = models.PositiveIntegerField(default=0)
    roles = models.ManyToManyField('Role')

    objects = AttachmentTypeManager()

    class Meta:
        app_label = 'misago'

    def update_roles(self, new_roles):
        self.roles.clear()
        for role in new_roles:
            self.roles.add(role)

    def normalize_extension(self, extension):
        extension = extension.lower()
        try:
            while extension[0] == '.':
                extension = extension[1:]
        except IndexError:
            return None
        return extension

    def has_extension(self, extension):
        extension = self.normalize_extension(extension)
        if extension:
            return extension in self.extensions.split(',')
        return False

    def file_of_type(self, filename):
        filename = filename.strip().lower()
        for extension in self.extensions.split(','):
            if filename[(len(extension) + 1) * -1:] == '.%s' % extension:
                return True
        return False

    def allow_file_upload(self, user, acl_limit, filesize):
        filesize /= 1024
        if self.roles_pks:
            user_roles = set(r.pk for r in user.roles.iterator())
            if not list(user_roles & self.roles_pks):
                raise ValidationError(_("You are not allowed to upload files of this type."))

        if acl_limit != 0:
            if self.size_limit and self.size_limit < acl_limit:
                size_limit = self.size_limit
            else:
                size_limit = acl_limit
            if filesize > size_limit:
                raise ValidationError(_("You are not allowed to upload files of this type that are larger than %(size)sKB.") % {'size': filesize})


