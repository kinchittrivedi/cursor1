import os
import json
from typing import List, Dict, Any, Tuple

INDEX_DIR = "/workspace/faiss_index"


class Retriever:
	def __init__(self) -> None:
		self._ready = os.path.exists(os.path.join(INDEX_DIR, "index.faiss")) and os.path.exists(os.path.join(INDEX_DIR, "meta.json"))
		self._meta: List[Dict[str, Any]] = []
		if self._ready:
			try:
				self._meta = json.load(open(os.path.join(INDEX_DIR, "meta.json")))
			except Exception:
				self._ready = False

	def is_ready(self) -> bool:
		return self._ready

	def search(self, query: str, k: int = 5) -> List[Tuple[float, Dict[str, Any]]]:
		return []