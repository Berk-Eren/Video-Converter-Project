from fastapi import FastAPI, Body, UploadFile, status, HTTPException, Path, Header, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security.api_key import APIKeyHeader

from gateway.client import auth_client
from gateway.forms.authentication import UserCreation, UserCredentials
from gateway.mongodb.save_file import save_into_db
from gateway.utils import log_in_user
from gateway.mq import send_message_to


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

    if user_logged_in:
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

@app.post("/download/{file_id}", response_class=FileResponse)
def download_converted_file(file_id: int = Path(ge=0)):
    #file = get_converted_file(file_id)
    return "out.mp4"
