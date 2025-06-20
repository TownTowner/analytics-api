from audioop import avg
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, and_, desc, select, func, case
from timescaledb.utils import get_utc_now
from timescaledb.hyperfunctions import time_bucket
from faker import Faker
import random
from datetime import datetime, timedelta
from typing import List

from .models import *
from api.db.session import get_session

eventRT = APIRouter()
EVENT_NAMES = ["/about", "/contact", "/pages", "/pricing"]


@eventRT.get("/", response_model=List[EventBucketSchema])
async def read_events(
    duration: str = Query(default="1 day"),
    pages: List = Query(default=None),
    session: Session = Depends(get_session),
) -> List[EventBucketSchema]:
    # query = select(EventModel).order_by(desc(EventModel.id))
    # print(duration, pages)
    # a bunch of items in a table
    ua_not_none = EventModel.user_agent.isnot(None)
    os_case = case(
        (
            and_(ua_not_none, EventModel.user_agent.ilike("%windows%")),
            "Windows",
        ),
        (
            and_(ua_not_none, EventModel.user_agent.ilike("%macintosh%")),
            "Macos",
        ),
        (
            and_(ua_not_none, EventModel.user_agent.ilike("%iphone%")),
            "ios",
        ),
        (
            and_(ua_not_none, EventModel.user_agent.ilike("%android%")),
            "Android",
        ),
        (
            and_(ua_not_none, EventModel.user_agent.ilike("%linux%")),
            "Linux",
        ),
        else_="other",
    ).label("operating_system")
    bucket = time_bucket(duration, EventModel.time)
    start = datetime.now() - timedelta(hours=1)
    finish = datetime.now() + timedelta(hours=1)
    pages = pages if isinstance(pages, list) and len(pages) > 0 else EVENT_NAMES
    query = (
        select(
            bucket.label("bucket"),
            os_case,
            func.avg(EventModel.duration).label("avg_duration"),
            EventModel.name.label("name"),
            func.count().label("count"),
        )
        .where(
            EventModel.duration > 0,
            # EventModel.time > start,
            # EventModel.time <= finish,
            EventModel.name.in_(pages),
        )
        .group_by(
            bucket,
            os_case,
            EventModel.name,
        )
        .order_by(
            bucket,
            os_case,
            EventModel.name,
        )
    )

    result = session.exec(query).fetchall()
    return result


@eventRT.get("/{event_id}", response_model=EventModel)
async def read_event(
    event_id: int, session: Session = Depends(get_session)
) -> EventModel:
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")

    return result


@eventRT.post("/", response_model=EventModel)
async def create_event(
    data: EventCreateSchema, session: Session = Depends(get_session)
) -> EventModel:
    # print(f"POST: {data}")
    item = data.model_dump()
    db_event = EventModel.model_validate(item)
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


@eventRT.post("/batchinsert")
async def create_events(session: Session = Depends(get_session)):
    names = [
        "/",
        "/about",
        "/pricing",
        "/contact",
        "/blog",
        "/products",
        "/login",
        "/signup",
        "/dashboard",
        "/settings",
    ]
    fake = Faker()
    session_ids = [fake.uuid4() for _ in range(200)]
    referrers = [
        "https://google.com",
        "https://facebook.com",
        "https://twitter.com",
        "https://linkedin.com",
        "",  # direct traffic
        "https://github.com",
    ]
    user_agents = [fake.safari, fake.chrome, fake.firefox, fake.opera, fake.user_agent]

    # query = select(EventModel).where(EventModel.user_agent == None)
    # result = session.exec(query).all()
    # print(len(result))
    # return
    for i in range(400):
        # for r in result:
        r = EventModel()
        r.name = random.choice(names)
        r.session_id = random.choice(session_ids)
        r.referrer = random.choice(referrers)
        r.user_agent = random.choice(user_agents)()
        r.ip_address = fake.ipv4()
        r.duration = random.randint(5, 300)
        session.add(r)

    session.commit()
    return {"message": "Events created"}


# @eventRT.put("/{event_id}", response_model=EventModel)
# async def update_event(
#     event_id: int, data: EventUpdateSchema, session: Session = Depends(get_session)
# ) -> EventModel:
#     print(f"PUT: {data}")
#     if event_id <= 0:
#         raise HTTPException(status_code=400, detail="Event ID must be greater than 0")

#     item = data.model_dump(exclude_unset=True)
#     if not item:
#         raise HTTPException(status_code=400, detail="No data to update")

#     query = select(EventModel).where(EventModel.id == event_id)
#     result = session.exec(query).first()
#     if not result:
#         raise HTTPException(status_code=404, detail="Event not found")

#     for key, value in item.items():
#         setattr(result, key, value)

#     result.update_at = get_utc_now()
#     session.add(result)
#     session.commit()
#     session.refresh(result)
#     return result  # type: ignore
