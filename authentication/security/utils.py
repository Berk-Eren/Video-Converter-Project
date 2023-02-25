from jose import JWTError, jwt
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from database.crud import get_user_by_name
from settings import (ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, 
                        SECRET_KEY )


def get_user_from_token(db, token):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_name(db, username=username)

    if user is None:
        raise credentials_exception

    return user

def create_token(username, expires_delta=None):
    to_encode = {
        "sub": username
    }

    if expires_delta:
        expire = timedelta(minutes=expires_delta)
    else:
        expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expire

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
