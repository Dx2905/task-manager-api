# from pydantic import BaseModel
# from typing import Optional


# class TaskBase(BaseModel):
#     title: str
#     description: Optional[str] = None
#     is_completed: Optional[bool] = False


# class TaskCreate(TaskBase):
#     pass


# class TaskUpdate(BaseModel):
#     title: Optional[str] = None
#     description: Optional[str] = None
#     is_completed: Optional[bool] = None


# class TaskOut(TaskBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True

from pydantic import BaseModel, ConfigDict
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: Optional[bool] = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class TaskOut(TaskBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)

