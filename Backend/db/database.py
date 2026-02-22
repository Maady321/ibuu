from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

IS_SQLITE = False

if not DATABASE_URL:
    logger.warning("DATABASE_URL not set — using local SQLite fallback!")
    DATABASE_URL = "sqlite:///./homebuddy.db"
    IS_SQLITE = True

# FOR VERCEL/SERVERLESS: ULTIMATE PG8000 OVERRIDE
# This replaces any scheme (e.g. postgres://, postgresql+psycopg2://, etc.)
# with the pure-Python pg8000 scheme.
if "://" in DATABASE_URL and "sqlite" not in DATABASE_URL:
    _, rest = DATABASE_URL.split("://", 1)
    DATABASE_URL = f"postgresql+pg8000://{rest}"
    logger.info("Database URL forced to postgresql+pg8000 dialect.")

# SQLite doesn't support pool_size / max_overflow — use StaticPool for it
if IS_SQLITE:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=5,
        max_overflow=10,
        echo=False,
    )

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

logger.info("Database engine created.")
