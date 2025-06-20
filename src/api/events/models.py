from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field
import sqlmodel
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now

CHUNK_TIME_INTERVAL = "INTERVAL 7 days"
DROP_AFTER = "INTERVAL 3 months"


class EventModel(TimescaleModel, table=True):
    name: str = Field(index=True)

    user_agent: Optional[str] = Field(default="", index=True)  # browser
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True)
    session_id: Optional[str] = Field(default="", index=True)
    duration: Optional[int] = Field(default=0)

    __chunk_time_interval__ = CHUNK_TIME_INTERVAL
    __drop_after__ = DROP_AFTER


class EventCreateSchema(SQLModel):
    name: str
    user_agent: Optional[str] = Field(default="", index=True)  # browser
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True)
    session_id: Optional[str] = Field(default="", index=True)
    duration: Optional[int] = Field(default=0)


# class EventUpdateSchema(SQLModel):
#     name: Optional[str]
#     description: Optional[str] = None


class EventListSchema(SQLModel):
    items: List[EventModel]
    count: int


class EventBucketSchema(SQLModel):
    bucket: datetime
    name: str
    operating_system: Optional[str]
    duration: Optional[float] = 0.0
    count: int
