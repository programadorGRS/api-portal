from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use a URL externa em vez da interna
DATABASE_URL = "postgresql://db_portal_grs_xkl3_user:mpmZlFvQSzxyTs43zc7WD1Leq2taCotm@dpg-cvav3jtrie7s739a7810-a.oregon-postgres.render.com/db_portal_grs_xkl3"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()