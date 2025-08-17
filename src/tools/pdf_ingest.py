import os
from typing import Tuple
from pypdf import PdfReader

REFERENCE_ROOT = "/workspace/content/reference"


def ensure_dir(path: str) -> None:
	os.makedirs(path, exist_ok=True)


def extract_text_from_pdf(pdf_path: str) -> Tuple[str, int]:
	reader = PdfReader(pdf_path)
	pages = len(reader.pages)
	texts = []
	for i in range(pages):
		page = reader.pages[i]
		texts.append(page.extract_text() or "")
	return "\n\n".join(texts), pages


def save_reference_text(source_name: str, text: str) -> str:
	doc_id = os.path.splitext(os.path.basename(source_name))[0]
	target_dir = os.path.join(REFERENCE_ROOT, doc_id)
	ensure_dir(target_dir)
	out_path = os.path.join(target_dir, "extracted.txt")
	with open(out_path, "w", encoding="utf-8") as f:
		f.write(text)
	return doc_id