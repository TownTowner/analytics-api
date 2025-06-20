from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, desc, select

from .models import *
from api.db.session import get_session

eventRT = APIRouter()


@eventRT.get("/", response_model=EventListSchema)
async def read_events(session: Session = Depends(get_session)) -> EventListSchema:
    query = select(EventModel).order_by(desc(EventModel.id))
    result = session.exec(query).all()
    return EventListSchema(items=list(result), count=len(result))


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
    print(f"POST: {data}")
    item = data.model_dump()
    db_event = EventModel.model_validate(item)
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


@eventRT.put("/{event_id}", response_model=EventModel)
async def update_event(
    event_id: int, data: EventUpdateSchema, session: Session = Depends(get_session)
) -> EventModel:
    print(f"PUT: {data}")
    if event_id <= 0:
        raise HTTPException(status_code=400, detail="Event ID must be greater than 0")

    item = data.model_dump(exclude_unset=True)
    if not item:
        raise HTTPException(status_code=400, detail="No data to update")

    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")

    for key, value in item.items():
        setattr(result, key, value)

    result.update_at = get_utc_now()
    session.add(result)
    session.commit()
    session.refresh(result)
    return result  # type: ignore
