from enum import Enum
import uuid
from typing import Generic, List, Optional, TypeVar, Literal, Dict

import uuid_utils
from pydantic import BaseModel, ConfigDict, EmailStr, Field

SortType = Literal["asc", "desc"]

class StudentModel(BaseModel):
    """Container for a single student record"""

    # The primary key for the StudentModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    student_id: Optional[uuid.UUID] | None = Field(
        alias="_id", default_factory=uuid_utils.uuid7
    )
    name: str = Field(...)
    mobile: str = Field(..., max_length=19, unique=True)
    email: str = Field(..., unique=True)
    course: str = Field(...)
    gpa: float = Field(..., le=4.0)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "mobile": "+12125555555",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": 3.0,
            }
        },
    )


class StudentPayload(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile: Optional[str] = Field(max_length=20, default=None)
    course: Optional[str] = None
    gpa: Optional[float] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "mobile": "+12125555555",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": 3.0,
            }
        },
    )

class Filter(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(1000, gt=0, le=1000)

class Paginate(Filter):
    name: Optional[SortType] = None
    email: Optional[SortType] = None
    mobile: Optional[SortType] = None
    course: Optional[SortType] = None
    gpa: Optional[SortType] = None

class StudentSearch(StudentPayload, Filter):
    """
    A set of optional updates to be made to a document in the database.
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "mobile": "+12125555555",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": 3.0,
                "offset": "0",
                "limit": "1000",
            }
        },
    )


class StudentCollection(BaseModel):
    """
    A container holding a list of `StudentModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    students: List[StudentModel]


T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: List[T]
    total_items: int


class StudentPage(BaseModel):
    items: List[StudentModel]
    total_items: int


class NotificationStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"

class NotificationModel(BaseModel):
    """Container for a single notification record"""

    notification_id: Optional[uuid.UUID] | None = Field(
        alias="_id", default_factory=uuid_utils.uuid7
    )
    name: str = Field(...)
    delivery: str = Field(...)
    contacts: List[str] = Field(...)
    status: NotificationStatus
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Semster Report",
                "delivery": "sms",
                "contacts": "['+12125555555']",
                "status": "completed"
            }
        },
    )

class NotificationPage(BaseModel):
    items: List[NotificationModel]
    total_items: int

class NotificationSearch(BaseModel):
    """Container for a notification search"""

    name: Optional[str] = None
    delivery: Optional[str] = None
    status: Optional[str] = None
    total_sent: Optional[int] = Field(default=0)
    total_failed: Optional[int] = Field(default=0)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Semster Report",
                "delievery": "sms",
                "status": "completed"
            }
        },
    )
