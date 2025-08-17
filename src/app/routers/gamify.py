from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from ..db import get_session
from ..models import GamificationState

router = APIRouter()


@router.get("/state/{student_id}")
def get_gamification_state(student_id: int):
	with get_session() as session:
		state = session.scalars(select(GamificationState).where(GamificationState.student_id == student_id)).first()
		if not state:
			return {"error": "not_found"}
		return {
			"xp": state.xp,
			"level": state.level,
			"streak_days": state.streak_days,
			"hearts": state.hearts,
			"league": state.league,
			"badges": state.badges.split(",") if state.badges else [],
			"total_correct": state.total_correct,
			"total_attempts": state.total_attempts,
		}