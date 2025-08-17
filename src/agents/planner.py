from __future__ import annotations
from typing import List
from ..tools.librarian import Librarian
from ..tools.progress_store import ProgressStore


class PlannerAgent:
	def __init__(self) -> None:
		self.librarian = Librarian()
		self.progress = ProgressStore()

	def select_next_skill(self, student_id: int, chapter_id: str) -> str:
		skills = self.librarian.get_skills_for_chapter(chapter_id)
		if not skills:
			return "general"
		# pick the lowest mastery skill, with tie-breaker on least recently updated
		masteries = {skill: self.progress.get_mastery(student_id, chapter_id, skill) for skill in skills}
		ordered = sorted(masteries.items(), key=lambda kv: kv[1])
		return ordered[0][0]