from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
from .models import UserRole

class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    role: UserRole
    is_active: bool
    created_at: Optional[str]

    class Config:
        orm_mode = True  # Important! Allows SQLAlchemy models to be converted to Pydantic


# Response model for login endpoint
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Role Enum must match the database model
class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"
    client = "client"


# Base schema shared by create & response schemas
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: UserRole = UserRole.client


# Schema used when creating a user (includes password)
class UserCreate(UserBase):
    password: str


# Schema returned in API responses (hides password)
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True  # Allows conversion from SQLAlchemy models

from pydantic import BaseModel
from typing import Optional
import enum
from datetime import datetime

class ProjectStatus(str, enum.Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[ProjectStatus] = ProjectStatus.PLANNING


class ProjectCreate(ProjectBase):
    manager_id: int


class ProjectOut(ProjectBase):
    id: int
    created_at: datetime
    manager_id: int

    class Config:
        orm_mode = True


class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.TODO


class TaskCreate(TaskBase):
    project_id: int
    assignee_id: int


class TaskOut(TaskBase):
    id: int
    created_at: datetime
    project_id: int
    assignee_id: int

    class Config:
        orm_mode = True

class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketBase(BaseModel):
    subject: str
    description: Optional[str] = None
    status: Optional[TicketStatus] = TicketStatus.OPEN


class TicketCreate(TicketBase):
    client_id: int
    assigned_to_id: Optional[int] = None


class TicketOut(TicketBase):
    id: int
    created_at: datetime
    client_id: int
    assigned_to_id: Optional[int] = None

    class Config:
        orm_mode = True


from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: Optional[str]
    status: Optional[str] = "Pending"
    priority: Optional[str] = "Medium"
    project_id: int
    assigned_to: Optional[int]

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    project_id: int
    assigned_to: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True
