from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///sh5.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def init_db():
    with engine.connect() as conn:
        conn.execute(text("PRAGMA journal_mode=WAL;"))
        conn.commit()

init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()