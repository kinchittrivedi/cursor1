from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class StudentCreate(BaseModel):
	name: str
	grade: int = 8


class StudentOut(BaseModel):
	id: int
	name: str
	grade: int

	class Config:
		from_attributes = True


class StartStudyRequest(BaseModel):
	student_id: int
	chapter_id: str
	mode: str = Field(default="study", pattern="^(study|quiz)$")


class Question(BaseModel):
	id: str
	prompt: str
	options: Optional[List[str]] = None
	question_type: str
	metadata: Dict[str, Any] = {}


class SubmitAnswerRequest(BaseModel):
	student_id: int
	chapter_id: str
	skill_id: str
	question_id: str
	answer: str


class SubmitAnswerResponse(BaseModel):
	is_correct: bool
	rationale: str
	xp_awarded: int
	hearts_remaining: int
	badges_earned: List[str] = []
	updated_mastery: float
	coach_action: Optional[str] = None