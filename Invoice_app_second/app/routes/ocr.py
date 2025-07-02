# app/routes/ocr.py

from fastapi import APIRouter, UploadFile, File
from app.services.ocr_engine import ocr_page_with_nanonets
import os, shutil

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

@router.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[-1]
    temp_path = os.path.join(UPLOAD_DIR, f"ocr_input{suffix}")
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    markdown = ocr_page_with_nanonets(temp_path)
    return {"ocr_output": markdown}
