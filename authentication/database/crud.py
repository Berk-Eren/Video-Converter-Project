from sqlalchemy.orm import Session

from . import models, schemas


model = models.User


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def login_user(db: Session, username: str, password: str):
    return db.query(models.User).filter(models.User.username==username).filter(models.User.password==password).first()

def get_user_by_email(db: Session, email: str, username: str):
    db_query = db.query(model)
    print(db_query.filter(model.username == username).first())

    if (user:=db_query.filter(model.email == email).first()):
        return user, "Email already registered"
    elif (user:=db_query.filter(model.username == username).first()):
        return user, "Username already registered"
    
    return None, ""

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, 
                            username=user.username, 
                                password=user.password )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
