from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, Boolean, UniqueConstraint, JSON
from .db import Base
from datetime import datetime


class Student(Base):
	__tablename__ = "students"
	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	name: Mapped[str] = mapped_column(String, nullable=False)
	grade: Mapped[int] = mapped_column(Integer, default=8)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

	progress = relationship("Progress", back_populates="student", cascade="all, delete-orphan")
	attempts = relationship("Attempt", back_populates="student", cascade="all, delete-orphan")
	gamestate = relationship("GamificationState", back_populates="student", uselist=False, cascade="all, delete-orphan")


class Progress(Base):
	__tablename__ = "progress"
	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
	chapter_id: Mapped[str] = mapped_column(String, index=True)
	skill_id: Mapped[str] = mapped_column(String, index=True)
	mastery: Mapped[float] = mapped_column(Float, default=0.0)
	last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

	student = relationship("Student", back_populates="progress")
	__table_args__ = (UniqueConstraint("student_id", "chapter_id", "skill_id", name="uq_progress"),)


class Attempt(Base):
	__tablename__ = "attempts"
	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
	chapter_id: Mapped[str] = mapped_column(String, index=True)
	skill_id: Mapped[str] = mapped_column(String, index=True)
	question_id: Mapped[str] = mapped_column(String)
	is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
	score_delta: Mapped[float] = mapped_column(Float, default=0.0)
	misconception_tags: Mapped[str] = mapped_column(String, default="")
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

	student = relationship("Student", back_populates="attempts")


class GamificationState(Base):
	__tablename__ = "gamification_state"
	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True, unique=True)
	xp: Mapped[int] = mapped_column(Integer, default=0)
	level: Mapped[int] = mapped_column(Integer, default=1)
	streak_days: Mapped[int] = mapped_column(Integer, default=0)
	last_active_date: Mapped[str] = mapped_column(String, default="")
	hearts: Mapped[int] = mapped_column(Integer, default=5)
	league: Mapped[str] = mapped_column(String, default="Bronze")
	badges: Mapped[str] = mapped_column(String, default="")  # comma-separated badge ids
	total_correct: Mapped[int] = mapped_column(Integer, default=0)
	total_attempts: Mapped[int] = mapped_column(Integer, default=0)

	student = relationship("Student", back_populates="gamestate")


class EventLog(Base):
	__tablename__ = "event_log"
	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	student_id: Mapped[int] = mapped_column(Integer, index=True)
	event_type: Mapped[str] = mapped_column(String)
	payload: Mapped[dict] = mapped_column(JSON)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)