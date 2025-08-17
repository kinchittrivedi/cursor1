import json
import os
from typing import List, Dict, Any

CONTENT_ROOT = "/workspace/content"


class Librarian:
	def __init__(self, root: str = CONTENT_ROOT) -> None:
		self.root = root

	def list_chapters(self) -> List[str]:
		if not os.path.isdir(self.root):
			return []
		return [name for name in os.listdir(self.root) if os.path.isdir(os.path.join(self.root, name))]

	def get_skills_for_chapter(self, chapter_id: str) -> List[str]:
		glossary_path = os.path.join(self.root, chapter_id, "glossary.json")
		if not os.path.exists(glossary_path):
			return []
		data = json.load(open(glossary_path))
		return sorted({entry["term"] for entry in data})[:20] or ["general"]

	def load_questions(self, chapter_id: str) -> List[Dict[str, Any]]:
		path = os.path.join(self.root, chapter_id, "questions.json")
		if not os.path.exists(path):
			return []
		return json.load(open(path))

	def load_tests(self, chapter_id: str) -> Dict[str, Any]:
		path = os.path.join(self.root, chapter_id, "tests.json")
		return json.load(open(path)) if os.path.exists(path) else {}

	def load_numericals(self, chapter_id: str) -> List[Dict[str, Any]]:
		path = os.path.join(self.root, chapter_id, "numericals.json")
		return json.load(open(path)) if os.path.exists(path) else []