import os
import json
from sentence_transformers import SentenceTransformer
import numpy as np

try:
	import faiss  # type: ignore
except Exception as e:
	faiss = None

CONTENT_ROOT = "/workspace/content"
INDEX_DIR = "/workspace/faiss_index"


def iter_chunks(text: str, chunk_size: int = 256, overlap: int = 40):
	words = text.split()
	start = 0
	while start < len(words):
		end = min(len(words), start + chunk_size)
		yield " ".join(words[start:end])
		start = end - overlap
		if start < 0:
			start = 0


def load_docs():
	for chapter_id in os.listdir(CONTENT_ROOT):
		cdir = os.path.join(CONTENT_ROOT, chapter_id)
		if not os.path.isdir(cdir):
			continue
		for fname in ["overview.md", "exposition.md", "activities.md", "misconceptions.md"]:
			path = os.path.join(cdir, fname)
			if os.path.exists(path):
				text = open(path, "r", encoding="utf-8").read()
				for i, chunk in enumerate(iter_chunks(text)):
					yield {"chapter_id": chapter_id, "file": fname, "chunk": i, "text": chunk}


def main():
	os.makedirs(INDEX_DIR, exist_ok=True)
	model = SentenceTransformer("all-MiniLM-L6-v2")
	meta = list(load_docs())
	if not meta:
		print("No content to index.")
		return
	embs = model.encode([m["text"] for m in meta]).astype("float32")
	if faiss is None:
		print("FAISS not installed; index will not be created.")
		return
	index = faiss.IndexFlatIP(embs.shape[1])
	faiss.normalize_L2(embs)
	index.add(embs)
	faiss.write_index(index, os.path.join(INDEX_DIR, "index.faiss"))
	json.dump(meta, open(os.path.join(INDEX_DIR, "meta.json"), "w", encoding="utf-8"))
	print(f"Indexed {len(meta)} chunks from content.")


if __name__ == "__main__":
	main()