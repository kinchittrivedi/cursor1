from __future__ import annotations
from typing import List
from ..tools.librarian import Librarian
from ..tools.progress_store import ProgressStore


class CoachAgent:
	def __init__(self) -> None:
		self.librarian = Librarian()
		self.progress = ProgressStore()

	def reteach(self, student_id: int, chapter_id: str, skill_id: str, misconception_tags: List[str]) -> str:
		# simple policy: log reteach action; could enqueue targeted explanation cards
		self.progress.log_event(student_id, "reteach", {"chapter_id": chapter_id, "skill_id": skill_id, "tags": misconception_tags})
		return "reteach_triggered"