from constants import BOOK_IMAGE_UPLOAD_PATH


def get_book_image_upload_path(instance, filename):
    """
    For generating a path from media root for uploading a book image
    Ex. books/book_name/filename
    """
    return "{}/{}/{}".format(
        BOOK_IMAGE_UPLOAD_PATH, 
        instance.name, 
        filename   # image name
    )
