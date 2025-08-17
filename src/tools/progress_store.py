from __future__ import annotations
from typing import Optional, Dict, Any
from sqlalchemy import select
from ..app.db import get_session
from ..app.models import Progress, Attempt, EventLog, GamificationState


class ProgressStore:
	def record_attempt(self, student_id: int, chapter_id: str, skill_id: str, question_id: str, is_correct: bool, misconception_tags: str, score_delta: float) -> None:
		with get_session() as session:
			attempt = Attempt(
				student_id=student_id,
				chapter_id=chapter_id,
				skill_id=skill_id,
				question_id=question_id,
				is_correct=is_correct,
				misconception_tags=misconception_tags,
				score_delta=score_delta,
			)
			session.add(attempt)
			state = session.scalars(select(GamificationState).where(GamificationState.student_id == student_id)).first()
			if state:
				state.total_attempts += 1
				if is_correct:
					state.total_correct += 1
			session.commit()

	def update_mastery(self, student_id: int, chapter_id: str, skill_id: str, delta: float) -> float:
		with get_session() as session:
			row = session.scalars(select(Progress).where(Progress.student_id == student_id, Progress.chapter_id == chapter_id, Progress.skill_id == skill_id)).first()
			if not row:
				row = Progress(student_id=student_id, chapter_id=chapter_id, skill_id=skill_id, mastery=0.0)
				session.add(row)
			row.mastery = max(0.0, min(1.0, (row.mastery or 0.0) + delta))
			session.commit()
			return row.mastery

	def get_mastery(self, student_id: int, chapter_id: str, skill_id: str) -> float:
		with get_session() as session:
			row = session.scalars(select(Progress).where(Progress.student_id == student_id, Progress.chapter_id == chapter_id, Progress.skill_id == skill_id)).first()
			return row.mastery if row else 0.0

	def log_event(self, student_id: int, event_type: str, payload: Dict[str, Any]) -> None:
		with get_session() as session:
			log = EventLog(student_id=student_id, event_type=event_type, payload=payload)
			session.add(log)
			session.commit()

	def get_gamestate(self, student_id: int) -> GamificationState | None:
		with get_session() as session:
			return session.scalars(select(GamificationState).where(GamificationState.student_id == student_id)).first()

	def save_gamestate(self, state: GamificationState) -> None:
		with get_session() as session:
			session.merge(state)
			session.commit()