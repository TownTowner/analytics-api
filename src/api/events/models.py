from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import SQLModel, Field
import sqlmodel


def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)


class EventModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # =  Field(default="")
    description: Optional[str] = None
    create_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False,
    )
    update_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False,
    )
    # start_date: str
    # end_date: str
    # location: str


class EventCreateSchema(SQLModel):
    name: str


class EventUpdateSchema(SQLModel):
    name: Optional[str]
    description: Optional[str] = None


class EventListSchema(SQLModel):
    items: List[EventModel]
    count: int
