from sqlmodel import create_engine, Session
import os

db_location = os.environ.get("DB_LOCATION", ".")

engine = create_engine(
  f"sqlite:///{db_location}/carsharing.db",
  connect_args={"check_same_thread": False}, # Needed for SQLite
  echo=True # Log generated SQL
)


def get_session():
    with Session(engine) as session:
        yield session
