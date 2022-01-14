from asgiref.sync import sync_to_async
from starlette.datastructures import UploadFile


@sync_to_async
def get_upload_size(upload: UploadFile) -> int:
    if not hasattr(upload, "_misago_file_size"):
        # TODO: remove this when UploadFile provides simpler way for checking size
        upload.file.seek(0, 2)  # Seek end of file
        upload._misago_file_size = upload.file.tell()  # type: ignore
        upload.file.seek(0, 0)

    return upload._misago_file_size  # type: ignore
