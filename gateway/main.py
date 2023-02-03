from fastapi import FastAPI, Body, UploadFile, status, HTTPException, Path, Header
from fastapi.responses import JSONResponse, FileResponse

from gateway.client import auth_client
from gateway.forms.authentication import UserCreation
from gateway.mongodb.save_file import save_into_db
from gateway.utils import log_in_user
from gateway.mq import send_message_to


app = FastAPI()


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

@app.post("/upload/", status_code=status.HTTP_202_ACCEPTED)
def create_upload_files(
    file: UploadFile,
    authorization: str = Header(default=None)
):
    user_logged_in = log_in_user(authorization)

    if user_logged_in:
        is_saved, file_id = save_into_db(file.file)
        if is_saved:
            send_message_to("video_conversion", str(file_id))
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

"""@app.post("/download/{file_id}")
def download_converted_file(file_id: int = Path(ge=0)):
    file = get_converted_file(file_id)
    return FileResponse(
        path="client.py",
        headers={
            "Content-Disposition": 'form-data; name="fieldName"; filename="output.mp3"'
        }
    )
"""