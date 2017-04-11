from rest_framework import viewsets
from rest_framework.response import Response

from django.core.exceptions import PermissionDenied, ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.threads.models import Attachment, AttachmentType
from misago.threads.serializers import AttachmentSerializer


IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif')


class AttachmentViewSet(viewsets.ViewSet):
    def create(self, request):
        if not request.user.acl_cache['max_attachment_size']:
            raise PermissionDenied(_("You don't have permission to upload new files."))

        try:
            return self.create_attachment(request)
        except ValidationError as e:
            return Response({'detail': e.args[0]}, status=400)

    def create_attachment(self, request):
        upload = request.FILES.get('upload')
        if not upload:
            raise ValidationError(_("No file has been uploaded."))

        user_roles = set(r.pk for r in request.user.get_roles())
        filetype = validate_filetype(upload, user_roles)
        validate_filesize(upload, filetype, request.user.acl_cache['max_attachment_size'])

        attachment = Attachment(
            secret=Attachment.generate_new_secret(),
            filetype=filetype,
            size=upload.size,
            uploader=request.user,
            uploader_name=request.user.username,
            uploader_slug=request.user.slug,
            uploader_ip=request.user_ip,
            filename=upload.name,
        )

        if is_upload_image(upload):
            try:
                attachment.set_image(upload)
            except IOError:
                raise ValidationError(_("Uploaded image was corrupted or invalid."))
        else:
            attachment.set_file(upload)

        attachment.save()
        add_acl(request.user, attachment)

        return Response(AttachmentSerializer(attachment, context={'user': request.user}).data)


def validate_filetype(upload, user_roles):
    filename = upload.name.strip().lower()

    queryset = AttachmentType.objects.filter(status=AttachmentType.ENABLED)
    for filetype in queryset.prefetch_related('limit_uploads_to'):
        for extension in filetype.extensions_list:
            if filename.endswith('.%s' % extension):
                break
        else:
            continue

        if filetype.mimetypes_list and upload.content_type not in filetype.mimetypes_list:
            continue

        if filetype.limit_uploads_to.exists():
            allowed_roles = set(r.pk for r in filetype.limit_uploads_to.all())
            if not user_roles & allowed_roles:
                continue

        return filetype

    raise ValidationError(_("You can't upload files of this type."))


def validate_filesize(upload, filetype, hard_limit):
    if upload.size > hard_limit * 1024:
        message = _("You can't upload files larger than %(limit)s (your file has %(upload)s).")
        raise ValidationError(
            message % {
                'upload': filesizeformat(upload.size).rstrip('.0'),
                'limit': filesizeformat(hard_limit * 1024).rstrip('.0'),
            }
        )

    if filetype.size_limit and upload.size > filetype.size_limit * 1024:
        message = _(
            "You can't upload files of this type larger than %(limit)s (your file has %(upload)s)."
        )
        raise ValidationError(
            message % {
                'upload': filesizeformat(upload.size).rstrip('.0'),
                'limit': filesizeformat(filetype.size_limit * 1024).rstrip('.0'),
            }
        )


def is_upload_image(upload):
    filename = upload.name.strip().lower()

    for extension in IMAGE_EXTENSIONS:
        if filename.endswith('.%s' % extension):
            return True
    return False
