from fastapi import APIRouter
from sqlalchemy import select, func
from ..db import get_session
from ..models import Progress, GamificationState, Student

router = APIRouter()


@router.get("/mastery/{student_id}")
def mastery_by_skill(student_id: int):
	with get_session() as session:
		rows = session.execute(select(Progress.chapter_id, Progress.skill_id, Progress.mastery).where(Progress.student_id == student_id)).all()
		return [{"chapter_id": r[0], "skill_id": r[1], "mastery": r[2]} for r in rows]


@router.get("/leaderboard")
def leaderboard():
	with get_session() as session:
		rows = session.execute(
			select(Student.name, GamificationState.xp)
			.join(GamificationState, GamificationState.student_id == Student.id)
			.order_by(GamificationState.xp.desc())
			.limit(50)
		).all()
		return [{"name": r[0], "xp": r[1]} for r in rows]