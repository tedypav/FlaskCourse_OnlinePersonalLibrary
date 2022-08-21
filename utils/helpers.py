import base64

from werkzeug.exceptions import BadRequest


def decode_file(path, encoded_string):
    with open(path, "wb") as f:
        try:
            f.write(base64.b64decode(encoded_string.encode("utf-8")))
        except Exception as ex:
            raise BadRequest("There is some problem with your file encoding. Please, make sure you ran it through a base64 encoder \N{slightly smiling face}")
