from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from ...tools.pdf_ingest import extract_text_from_pdf, save_reference_text

router = APIRouter()

UPLOAD_DIR = "/workspace/uploads"


@router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...)):
	if not file.filename.lower().endswith(".pdf"):
		raise HTTPException(status_code=400, detail="Only PDF files are supported")
	os.makedirs(UPLOAD_DIR, exist_ok=True)
	temp_path = os.path.join(UPLOAD_DIR, file.filename)
	with open(temp_path, "wb") as f:
		f.write(await file.read())
	text, pages = extract_text_from_pdf(temp_path)
	doc_id = save_reference_text(file.filename, text)
	return {"doc_id": doc_id, "pages": pages, "characters": len(text)}