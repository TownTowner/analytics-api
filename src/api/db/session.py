from sqlmodel import create_engine, Session, SQLModel
from api.db.config import DATABASE_URL


if DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)
    # session = Session(engine)
    # return session


def get_session():
    with Session(engine) as session:
        yield session
