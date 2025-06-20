from sqlmodel import Session, SQLModel
from .config import DATABASE_URL, DB_TIMEZONE
import timescaledb

if DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL is not set")

engine = timescaledb.create_engine(DATABASE_URL, timezone=DB_TIMEZONE)


def init_db():
    print("init db")
    SQLModel.metadata.create_all(engine)
    print("create timescaledb extension")
    timescaledb.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
