from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unnoti_corestore.utils.config_loader import Config

if not Config.DATABASE_URL:
    raise RuntimeError("DATABASE_URL not found (check .env or ENV vars)")

engine = create_engine(Config.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)