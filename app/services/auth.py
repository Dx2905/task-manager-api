from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.token import Token
from sqlalchemy.orm import Session
from app.models.user import User

from app.schemas.user import UserCreate, UserOut


from app.core.security import hash_password

def create_user(user_in: UserCreate, db: Session) -> UserOut:
    hashed_pw = hash_password(user_in.password)
    user = User(
    email=user_in.email,
    username=user_in.username,
    hashed_password=hashed_pw
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

from app.core.security import verify_password, create_access_token
from fastapi import HTTPException, status

def authenticate_user(email: str, password: str, db: Session) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def login_user(form_data: OAuth2PasswordRequestForm, db: Session) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)  # username = email
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")
