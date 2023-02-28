import os
import tempfile

from fastapi import FastAPI, Body, UploadFile, status, HTTPException, Path, Header, Depends, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security.api_key import APIKeyHeader

from client import auth_client
from forms.authentication import UserCreation, UserCredentials
from mongodb import save_into_db, get_converted_file
from utils import log_in_user
from mq import send_message_to

from utils.file_ops import close_file


app = FastAPI()
token_key = APIKeyHeader(name="Authorization")


@app.post("/sign-up/")
def login(user: UserCreation = Body()):
    user_credentials = {
        "email": user.email,
        "username": user.username,
        "password": user.password,
        "password2": user.password2
    }
    res = auth_client.post("/sign-up/", data=user_credentials)

    return res.json()

@app.post("/access-token/")
def get_access_token(user_credentials: UserCredentials):
    credentials = {
        "username": user_credentials.username,
        "password": user_credentials.password
    }
    res = auth_client.post("/access-token/", data=credentials)
    return res.json()

@app.post("/upload/", status_code=status.HTTP_202_ACCEPTED)
def create_upload_files(
    file: UploadFile,
    token: str | None = Depends(token_key)
):
    user_logged_in = log_in_user(token)

    if user_logged_in.status_code==200:
        is_saved, file_obj = save_into_db(file.file)
        if is_saved:
            file_id = str(file_obj)
            send_message_to("video_conversion_queue", file_id)
            return JSONResponse(content={
                "fileId": file_id
            })

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File couldn't be inserted into the database"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please check your credentials"
        )

@app.post("/download/{file_id}")
def download_converted_file(
    file_id: str = Path(min_length=1), 
    *, 
    background_task: BackgroundTasks
):
    converted_file_obj = get_converted_file(file_id)

    temp_file_obj = tempfile.NamedTemporaryFile()
    temp_file_obj.write(converted_file_obj.read())
    temp_file_path = os.path.join(tempfile.gettempdir(), 
                                    temp_file_obj.name)

    background_task.add_task(close_file, temp_file_obj)

    return FileResponse(path=temp_file_path, filename="output.mp3", 
                            media_type='application/octet-stream' )
