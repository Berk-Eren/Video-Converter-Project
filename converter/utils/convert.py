import os
import tempfile
from bson.objectid import ObjectId
import moviepy.editor as mp



class VideoToMP3Converter:
    def __init__(self, db):
        self.db = db
        self.__file_obj = None

    @property
    def file_obj(self):
        file_obj = self.__file_obj
        self.__file_obj = None
        return file_obj

    def convert_video_to_mp3(self, file_id):
        file_obj = self.db.get(ObjectId(file_id))

        with tempfile.NamedTemporaryFile() as file:
            file.write(file_obj.read())
            audio = mp.VideoFileClip(file.name).audio

            self.__temp_file_name = os.path.join(tempfile.gettempdir(), 
                                                "output.mp3")
            audio.write_audiofile(self.__temp_file_name)

    def save_converted_file_into_db(self):
        with open(self.__temp_file_name, "rb") as file:
            self.__file_obj = self.db.put(file.read())
