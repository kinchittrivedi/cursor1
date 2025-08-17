import os
import sys
from ..tools.content_builder import split_chapters, write_chapter_dir, normalize_space

CONTENT_ROOT = "/workspace/content"
REFERENCE_ROOT = "/workspace/content/reference"


def main(doc_id: str):
	ref_path = os.path.join(REFERENCE_ROOT, doc_id, "extracted.txt")
	if not os.path.exists(ref_path):
		raise SystemExit(f"Reference not found: {ref_path}")
	full_text = open(ref_path, "r", encoding="utf-8").read()
	chapters = split_chapters(full_text)
	if not chapters:
		raise SystemExit("No chapters detected in reference text.")
	for idx, (title, ch_text) in enumerate(chapters, start=1):
		chapter_id = f"ch{idx:02d}"
		write_chapter_dir(CONTENT_ROOT, chapter_id, title, normalize_space(ch_text))
	print(f"Generated {len(chapters)} chapters into {CONTENT_ROOT}")


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Usage: python -m src.scripts.ingest_reference <doc_id>")
		sys.exit(1)
	main(sys.argv[1])