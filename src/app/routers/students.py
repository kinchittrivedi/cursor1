from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from ..db import get_session, engine
from ..models import Student, GamificationState
from ..schemas import StudentCreate, StudentOut

router = APIRouter()


@router.post("/", response_model=StudentOut)
def create_student(payload: StudentCreate):
	with get_session() as session:
		student = Student(name=payload.name, grade=payload.grade)
		session.add(student)
		session.flush()
		state = GamificationState(student_id=student.id)
		session.add(state)
		session.commit()
		return student


@router.get("/", response_model=list[StudentOut])
def list_students():
	with get_session() as session:
		students = session.scalars(select(Student)).all()
		return students