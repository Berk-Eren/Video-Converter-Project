from fastapi import FastAPI, HTTPException, Depends, Header, status
from sqlalchemy.orm import Session

from authentication.database import SessionLocal, engine
from authentication.database import schemas, crud, models
from authentication.security.utils import create_token, get_user_from_token
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
    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )

    return crud.create_user(db=db, user=user)

@app.post("/login/")
def get_access_token(db: Session = Depends(get_db), *, user: UserCredentials = Depends()):
    user = crud.login_user(db, user.username, user.password)
    return create_token(user.username)

@app.post("/refresh")
def refresh_token(header: str | None = Header()):
    pass
