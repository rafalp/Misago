from asgiref.sync import sync_to_async
from starlette.datastructures import UploadFile


@sync_to_async
def get_upload_size(upload: UploadFile) -> int:
    # TODO: remove this when UploadFile provides simpler way for checking size
    upload.file.seek(0, 2)  # Seek end of file
    file_size = upload.file.tell()
    upload.file.seek(0, 0)
    return file_size
