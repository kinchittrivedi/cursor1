import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////workspace/data/tutor.db")

engine = None
SessionLocal = None
Base = declarative_base()


def init_engine_and_session():
	global engine, SessionLocal
	os.makedirs("/workspace/data", exist_ok=True)
	engine = create_engine(
		DATABASE_URL,
		connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
		future=True,
	)
	SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine, future=True)
	return engine


def get_session():
	assert SessionLocal is not None, "Database session not initialized. Call init_engine_and_session() first."
	return SessionLocal()