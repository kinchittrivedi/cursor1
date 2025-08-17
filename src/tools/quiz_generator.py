import random
from typing import Dict, Any
from ..app.schemas import Question
from .librarian import Librarian


class QuizGenerator:
	def __init__(self, librarian: Librarian, retriever) -> None:
		self.librarian = librarian
		self.retriever = retriever

	def next_question(self, chapter_id: str, skill_id: str, mode: str = "study") -> Question:
		pool = self.librarian.load_questions(chapter_id)
		candidate = None
		for q in pool:
			if q.get("skill_id") == skill_id and q.get("question_type") == "mcq":
				candidate = q
				break
			
		if not candidate and pool:
			candidate = random.choice([q for q in pool if q.get("question_type") == "mcq"]) if pool else None

		if not candidate:
			return Question(id="fallback", prompt="Study material not found.", options=None, question_type="info", metadata={})

		return Question(
			id=candidate["id"],
			prompt=candidate["prompt"],
			options=candidate.get("options"),
			question_type=candidate.get("question_type", "mcq"),
			metadata={"skill_id": candidate.get("skill_id")},
		)