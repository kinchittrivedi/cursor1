from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from ..app.models import GamificationState
from ..app.db import get_session
from ..tools.progress_store import ProgressStore
from .config import GamificationConfig


@dataclass
class OutcomeEffects:
	xp_awarded: int
	hearts_remaining: int
	badges_earned: list[str]


class GamificationEngine:
	def __init__(self, progress: ProgressStore) -> None:
		self.progress = progress
		self.config = GamificationConfig()

	def _today(self) -> str:
		return datetime.now(timezone.utc).date().isoformat()

	def _update_streak(self, state: GamificationState) -> None:
		today = self._today()
		if state.last_active_date == today:
			return
		if not state.last_active_date:
			state.streak_days = 1
		else:
			prev = datetime.fromisoformat(state.last_active_date).date()
			curr = datetime.fromisoformat(today).date()
			if (curr - prev).days == 1:
				state.streak_days += 1
			else:
				state.streak_days = 1
		state.last_active_date = today

	def apply_answer_outcome(self, student_id: int, is_correct: bool) -> OutcomeEffects:
		with get_session() as session:
			state = session.scalars(select(GamificationState).where(GamificationState.student_id == student_id)).first()
			if not state:
				state = GamificationState(student_id=student_id)
				session.add(state)

			self._update_streak(state)
			xp_gain = self.config.XP_CORRECT if is_correct else self.config.XP_INCORRECT
			state.xp += xp_gain
			if is_correct:
				state.level = max(1, 1 + state.xp // self.config.XP_PER_LEVEL)
			else:
				state.hearts = max(0, state.hearts - 1)

			badges = []
			for threshold, badge_id in self.config.CORRECT_BADGES:
				if state.total_correct >= threshold and badge_id not in state.badges.split(","):
					badges.append(badge_id)
			if badges:
				state.badges = ",".join(sorted(set(filter(None, state.badges.split(",") + badges))))

			session.commit()
			return OutcomeEffects(xp_awarded=xp_gain, hearts_remaining=state.hearts, badges_earned=badges)