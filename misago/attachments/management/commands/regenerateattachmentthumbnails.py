from io import BytesIO

from PIL import Image, UnidentifiedImageError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand, CommandError

from ....conf.dynamicsettings import DynamicSettings
from ....conf.shortcuts import get_dynamic_settings
from ...models import Attachment
from ...thumbnails import generate_attachment_thumbnail


class Command(BaseCommand):
    help = "Regenerates attachment thumbnails and updates image dimensions in the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "after",
            help="attachment ID to start processing from",
            nargs="?",
            type=int,
        )

    def handle(self, *args, **options):
        queryset = Attachment.objects.exclude(upload="").order_by("-id")
        if options["after"] is not None:
            after = options["after"]
            if after < 1:
                raise CommandError("'after' arg must be greater than 0")

            queryset = queryset.filter(id__lt=after)

        settings = get_dynamic_settings()

        self.stdout.write(f"Attachments to process: {queryset.count()}")
        self.stdout.write("\nProcessing:")

        for attachment in queryset.iterator(chunk_size=50):
            if not attachment.filetype.is_image:
                continue

            try:
                self.process_attachment(settings, attachment)
            except UnidentifiedImageError:
                self.stderr.write(
                    f"#{attachment.id}: {attachment.name} "
                    "-> cannot identify image file!"
                )

    def process_attachment(self, settings: DynamicSettings, attachment: Attachment):
        image = Image.open(attachment.upload.path)

        width, height = image.size
        attachment.dimensions = f"{width}x{height}"

        thumbnail_width = settings.attachment_thumbnail_width
        thumbnail_height = settings.attachment_thumbnail_height

        attachment.thumbnail_dimensions = None
        attachment.thumbnail_size = 0

        if attachment.thumbnail:
            attachment.thumbnail.delete()

        if width > thumbnail_width or height > thumbnail_height:
            generate_attachment_thumbnail(
                attachment, image, thumbnail_width, thumbnail_height
            )

        attachment.save(
            update_fields=[
                "dimensions",
                "thumbnail",
                "thumbnail_dimensions",
                "thumbnail_size",
            ]
        )

        self.stdout.write(f"#{attachment.id}: {attachment.name}")
