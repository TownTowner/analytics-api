from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import SQLModel, Field
import sqlmodel
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now

# def get_utc_now():
#     return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)

CHUNK_TIME_INTERVAL = "INTERVAL 7 days"
DROP_AFTER = "INTERVAL 3 months"


class EventModel(TimescaleModel, table=True):
    # id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)

    description: Optional[str] = None
    # create_at: datetime = Field(
    #     default_factory=get_utc_now,
    #     sa_type=sqlmodel.DateTime(timezone=True),
    #     nullable=False,
    # )
    update_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False,
    )

    __chunk_time_interval__ = CHUNK_TIME_INTERVAL
    __drop_after__ = DROP_AFTER


class EventCreateSchema(SQLModel):
    name: str


class EventUpdateSchema(SQLModel):
    name: Optional[str]
    description: Optional[str] = None


class EventListSchema(SQLModel):
    items: List[EventModel]
    count: int


class EventBucketSchema(SQLModel):
    bucket: datetime
    name: str
    count: int
