from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy.orm import Session

from authentication.database import SessionLocal, engine
from authentication.database import schemas, crud, models
from authentication.security.utils import create_token
from authentication.security.schemas import oauth2_scheme
from authentication.forms import UserCredentials


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/sign-up")
def sign_up(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    """
    return crud.create_user(db=db, user=user)

@app.post("/validate/")
def validate_token(header = Header()):
    pass

@app.post("/refresh")
def refresh_token(header: str | None = Header()):
    pass

@app.post("/login/")
def login_person(db: Session = Depends(get_db), form_data: UserCredentials = Depends()):
    user = crud.login_user(db, form_data.username, form_data.password)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Username or password is wrong. Please try again."
        )

    encoded_jwt = create_token(user.username)

    return encoded_jwt
