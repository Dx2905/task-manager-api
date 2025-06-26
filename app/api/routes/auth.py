# # from fastapi import APIRouter, Depends, HTTPException, status
# # from sqlalchemy.orm import Session
# # from app.schemas import user as user_schema
# # from app.services import auth as auth_service
# # from app.api.dependencies import get_db

# # router = APIRouter(prefix="/auth", tags=["Auth"])

# # @router.post("/signup", response_model=user_schema.UserOut, status_code=status.HTTP_201_CREATED)
# # def signup(user_in: user_schema.UserCreate, db: Session = Depends(get_db)):
# #     return auth_service.create_user(user_in, db)

# # @router.post("/login", response_model=schemas.Token)
# # def login(user_in: schemas.UserLogin, db: Session = Depends(get_db)):
# #     return auth_service.login_user(user_in, db)

# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from app.schemas.user import UserCreate, UserLogin, UserOut
# from app.schemas.token import Token
# from app.services import auth as auth_service
# from app.api.dependencies import get_db


# router = APIRouter(prefix="/auth", tags=["Auth"])

# @router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
# def signup(user_in: UserCreate, db: Session = Depends(get_db)):
#     return auth_service.create_user(user_in, db)

# @router.post("/login", response_model=Token)
# def login(user_in: UserLogin, db: Session = Depends(get_db)):
#     return auth_service.login_user(user_in, db)

# from app.models.user import User
# from app.api.dependencies import get_current_user

# @router.get("/me", response_model=UserOut)
# def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token
from app.services import auth as auth_service
from app.api.dependencies import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    return auth_service.create_user(user_in, db)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # `username` is the field OAuth2 expects; map it to email
    return auth_service.login_user(form_data, db)

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
