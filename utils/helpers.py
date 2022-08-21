import os

from constants import TEMP_FILE_FOLDER


def delete_local_file(name):
    try:
        os.remove(os.path.join(TEMP_FILE_FOLDER, name))
    except Exception as ex:
        raise ex
