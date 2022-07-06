from constants import (
    AUTHORS_PHOTO_UPLOAD_PATH,
    CLIENTS_PHOTO_UPLOAD_PATH,   
    CLIENT_MODEL_NAME
)


def get_user_photo_upload_path(instance, filename):
    """
    For generating a path from media root for uploading user photos.
    Ex. for client user  -->  clients/client_username/filename
    Ex. for author user  -->  authors/author_username/filename
    """
    user_model_name = type(instance).__name__

    if user_model_name == CLIENT_MODEL_NAME:
        return "{}/{}/{}".format(
            CLIENTS_PHOTO_UPLOAD_PATH, 
            instance.username, 
            filename
        )
    # else requesting user is an author
    return "{}/{}/{}".format(
        AUTHORS_PHOTO_UPLOAD_PATH,
        instance.username,
        filename
    )
