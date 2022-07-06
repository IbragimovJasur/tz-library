from constants import (
    AUTHORS_PHOTO_UPLOAD_PATH,
    CLIENTS_PHOTO_UPLOAD_PATH,
)


def get_client_photo_upload_path(instance, filename):
    """
    For generating a path from media root for uploading client user photo.
    Ex. for client user  -->  clients/client_username/filename
    """
    return "{}/{}/{}".format(
        CLIENTS_PHOTO_UPLOAD_PATH, 
        instance.user.username, 
        filename
    )


def get_author_photo_upload_path(instance, filename):
    """
    For generating a path from media root for uploading author user photo.
    Ex. for author user  -->  authors/author_username/filename
    """
    return "{}/{}/{}".format(
        AUTHORS_PHOTO_UPLOAD_PATH,
        instance.user.username,
        filename
    )
