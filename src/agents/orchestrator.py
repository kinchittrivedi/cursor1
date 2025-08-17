from typing import Optional
from ..app.schemas import Question, SubmitAnswerRequest, SubmitAnswerResponse
from .planner import PlannerAgent
from .tutor import TutorAgent
from .evaluator import EvaluatorAgent
from .coach import CoachAgent
from ..tools.progress_store import ProgressStore
from ..gamification.engine import GamificationEngine


class StudyOrchestrator:
	def __init__(self) -> None:
		self.planner = PlannerAgent()
		self.tutor = TutorAgent()
		self.evaluator = EvaluatorAgent()
		self.coach = CoachAgent()
		self.progress = ProgressStore()
		self.gamify = GamificationEngine(self.progress)

	async def start_session(self, student_id: int, chapter_id: str, mode: str = "study") -> Question:
		selected_skill = self.planner.select_next_skill(student_id, chapter_id)
		question = self.tutor.generate_question(chapter_id=chapter_id, skill_id=selected_skill, mode=mode)
		return question

	async def next_question(self, student_id: int, chapter_id: str, mode: str = "study") -> Question:
		selected_skill = self.planner.select_next_skill(student_id, chapter_id)
		return self.tutor.generate_question(chapter_id=chapter_id, skill_id=selected_skill, mode=mode)

	async def submit_answer(self, req: SubmitAnswerRequest) -> SubmitAnswerResponse:
		grading = self.evaluator.grade(req.chapter_id, req.skill_id, req.question_id, req.answer)
		self.progress.record_attempt(
			student_id=req.student_id,
			chapter_id=req.chapter_id,
			skill_id=req.skill_id,
			question_id=req.question_id,
			is_correct=grading.is_correct,
			misconception_tags=",".join(grading.misconception_tags),
			score_delta=grading.score_delta,
		)
		updated_mastery = self.progress.update_mastery(req.student_id, req.chapter_id, req.skill_id, grading.mastery_delta)

		coach_action = None
		if grading.misconception_tags:
			coach_action = self.coach.reteach(req.student_id, req.chapter_id, req.skill_id, grading.misconception_tags)

		effects = self.gamify.apply_answer_outcome(req.student_id, grading.is_correct)
		return SubmitAnswerResponse(
			is_correct=grading.is_correct,
			rationale=grading.rationale,
			xp_awarded=effects.xp_awarded,
			hearts_remaining=effects.hearts_remaining,
			badges_earned=effects.badges_earned,
			updated_mastery=updated_mastery,
			coach_action=coach_action,
		)