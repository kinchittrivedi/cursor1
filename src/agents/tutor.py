from __future__ import annotations
from typing import List, Optional
from ..app.schemas import Question
from ..tools.librarian import Librarian
from ..tools.retrieval import Retriever
from ..tools.quiz_generator import QuizGenerator


class TutorAgent:
	def __init__(self) -> None:
		self.librarian = Librarian()
		self.retriever = Retriever()
		self.quiz = QuizGenerator(self.librarian, self.retriever)

	def generate_question(self, chapter_id: str, skill_id: str, mode: str = "study") -> Question:
		# vary pedagogy: retrieval practice (MCQ) by default
		return self.quiz.next_question(chapter_id=chapter_id, skill_id=skill_id, mode=mode)