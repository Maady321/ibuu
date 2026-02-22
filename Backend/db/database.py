from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logger.error("CRITICAL: DATABASE_URL is not set! PostgreSQL is required.")
    # In production, we want to fail fast if the DB is misconfigured
    raise ValueError("Missing DATABASE_URL environment variable. PostgreSQL connection is mandatory.")

# FOR VERCEL/SERVERLESS: ULTIMATE PG8000 OVERRIDE
# This replaces any scheme (e.g. postgres://, postgresql+psycopg2://, etc.)
# with the pure-Python pg8000 scheme for maximum compatibility.
if "://" in DATABASE_URL:
    scheme, rest = DATABASE_URL.split("://", 1)
    if "postgresql" in scheme or scheme == "postgres":
        DATABASE_URL = f"postgresql+pg8000://{rest}"
        logger.info("Database URL finalized with postgresql+pg8000 dialect.")

# Create PostgreSQL engine with optimized pooling for serverless
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

logger.info("PostgreSQL database engine initialized.")
