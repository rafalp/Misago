from django.db import models

class AttachmentType(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    extensions = models.CharField(max_length=255)
    size_limit = models.PositiveIntegerField(default=0)
    roles = models.ManyToManyField('Role')

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