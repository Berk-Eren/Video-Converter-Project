from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from .database import schemas, crud, models


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/login", response_model=schemas.User)
def login(body: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.login_user(db, body.username, body.password)
    if user:
        return user
    raise HTTPException(status_code=404, detail="No such user is found.")


@app.post("/sign-up")
def sign_up(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    """
    return crud.create_user(db=db, user=user)


@app.post("/refresh")
def refresh_token():
    pass
