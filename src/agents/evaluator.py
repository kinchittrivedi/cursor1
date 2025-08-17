from __future__ import annotations
from dataclasses import dataclass
from typing import List
from ..tools.grader import Grader


@dataclass
class Grading:
	is_correct: bool
	rationale: str
	misconception_tags: List[str]
	score_delta: float
	mastery_delta: float


class EvaluatorAgent:
	def __init__(self) -> None:
		self.grader = Grader()

	def grade(self, chapter_id: str, skill_id: str, question_id: str, answer: str) -> Grading:
		result = self.grader.grade(chapter_id, skill_id, question_id, answer)
		mastery_delta = 0.05 if result.is_correct else -0.02
		return Grading(
			is_correct=result.is_correct,
			rationale=result.rationale,
			misconception_tags=result.misconception_tags,
			score_delta=1.0 if result.is_correct else 0.0,
			mastery_delta=mastery_delta,
		)