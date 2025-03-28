from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

DATABASE_URL = "sqlite:///game_database.db"
engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def db_session():
    session = scoped_session(SessionFactory)()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
