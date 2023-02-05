from .db import fs


def save_into_db(file):
    file_obj = fs.put(file.read())

    return fs.exists(file_obj), file_obj

def get_converted_file(file_id):
    return {}
