from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import Depends

from app.schemas.user import UserOut, UserUpdate
from app.models.user import User
from app.api.dependencies import get_db, get_current_user
from app.utils.authz import is_admin_or_self

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    # if not user or not is_admin_or_self(current_user, user_id):
    #     raise HTTPException(status_code=403, detail="Not authorized or user not found")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not is_admin_or_self(current_user, user_id):
        raise HTTPException(status_code=403, detail="Not authorized to view this user")

    return user


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")

    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not is_admin_or_self(current_user, user_id, admin_only=True):
        raise HTTPException(status_code=403, detail="Only admins can delete users")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
