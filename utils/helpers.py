import os

from constants import TEMP_FILE_FOLDER


def delete_local_file(name):
    """
    Deletes a file from the local temp folder. By default it uses the location to the temp folder in the project.
    :param name: string, the name of the file to be deleted
    :return Nothing if the delete is successful; Errors if the delete is unsuccessful
    """
    try:
        os.remove(os.path.join(TEMP_FILE_FOLDER, name))
    except Exception as ex:
        raise ex
