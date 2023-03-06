from fastapi import FastAPI, HTTPException, Body, Depends, Header, status
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from database import schemas, crud, models
from security.utils import create_token, get_user_from_token
from security.schemas import oauth2_scheme
from forms import UserCredentials


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/sign-up/", status_code=status.HTTP_201_CREATED)
def sign_up(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user, msg = crud.get_user_by_email(db, user.email, user.username)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=msg
        )

    return crud.create_user(db=db, user=user)

@app.post("/access-token/")
def get_access_token(user: UserCredentials = Depends(), db: Session = Depends(get_db)):
    user = crud.login_user(db, user.username, user.password)
    if user:
        return create_token(user.username)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Please check your credentials"
    )

@app.post("/validate/")
def validate_token(authorization: str = Header(), db: Session = Depends(get_db)):
    token_type, token = authorization.split()
    return get_user_from_token(db, token)

@app.post("/refresh")
def refresh_token(header: str | None = Header()):
    pass
