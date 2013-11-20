from misago.models import AttachmentType
from misago.utils.translation import ugettext_lazy as _

def load():
    AttachmentType.objects.create(
        name=_('Image file').message,
        extensions='gif,jpg,jpeg,png',
        size_limit=0,
    )

    AttachmentType.objects.create(
        name=_('Archive').message,
        extensions='rar,zip,7z,tar.gz',
        size_limit=0,
    )

    AttachmentType.objects.create(
        name=_('Document').message,
        extensions='pdf,txt,doc,docx,xls,xlsx,xlsm,xlsb',
        size_limit=0,
    )