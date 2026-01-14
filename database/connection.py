from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Connects the SQLAlchemy library to the database.
engine = create_engine('postgresql+psycopg://?????:????@localhost:5432/dentist_clinic')

# By default, it creates 5 connection pools.
session_local = sessionmaker(bind = engine, autoflush = False, autocommit = False)

Base = declarative_base()


def create_tables():
    # transform all models into tables, creating all the tables.
    Base.metadata.create_all(bind = engine)


def get_connection():
    # opens a connection to the pools
    session = session_local()

    try:
        # Pause the connection until FastAPI finishes processing the request.
        yield session

    finally:
        session.close()
