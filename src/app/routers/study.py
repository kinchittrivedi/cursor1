from fastapi import APIRouter, HTTPException
from ..schemas import StartStudyRequest, Question, SubmitAnswerRequest, SubmitAnswerResponse
from ...agents.orchestrator import StudyOrchestrator

router = APIRouter()

orchestrator = StudyOrchestrator()


@router.post("/start", response_model=Question)
async def start_study(req: StartStudyRequest):
	question = await orchestrator.start_session(student_id=req.student_id, chapter_id=req.chapter_id, mode=req.mode)
	return question


@router.post("/next", response_model=Question)
async def next_question(req: StartStudyRequest):
	question = await orchestrator.next_question(student_id=req.student_id, chapter_id=req.chapter_id, mode=req.mode)
	return question


@router.post("/submit", response_model=SubmitAnswerResponse)
async def submit_answer(req: SubmitAnswerRequest):
	resp = await orchestrator.submit_answer(req)
	return resp