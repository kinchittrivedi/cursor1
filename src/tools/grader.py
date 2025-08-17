from typing import List
from dataclasses import dataclass
from .librarian import Librarian


@dataclass
class GradeResult:
	is_correct: bool
	rationale: str
	misconception_tags: List[str]


class Grader:
	def __init__(self) -> None:
		self.librarian = Librarian()

	def grade(self, chapter_id: str, skill_id: str, question_id: str, answer: str) -> GradeResult:
		pool = self.librarian.load_questions(chapter_id)
		q = next((x for x in pool if x.get("id") == question_id), None)
		if not q:
			return GradeResult(False, "Question not found.", ["data_missing"])
		correct_answer = q.get("answer")
		if q.get("question_type") == "mcq":
			is_correct = (answer.strip().lower() == str(correct_answer).strip().lower())
			rationale = q.get("rationale", "")
			miscon = q.get("misconception_tags", []) if not is_correct else []
			return GradeResult(is_correct, rationale, miscon)
		# simple fallback
		is_correct = answer.strip().lower() == str(correct_answer).strip().lower()
		rationale = q.get("rationale", "")
		miscon = ["incomplete_reasoning"] if not is_correct else []
		return GradeResult(is_correct, rationale, miscon)