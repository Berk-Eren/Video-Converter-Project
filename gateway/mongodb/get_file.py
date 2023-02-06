from .db import fs
from bson.objectid import ObjectId


def get_converted_file(file_id):
    return fs.get(ObjectId(file_id))
