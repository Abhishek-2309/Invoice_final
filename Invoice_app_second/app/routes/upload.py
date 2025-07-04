# app/routes/upload.py

import os, shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
from httpx import AsyncClient

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

@router.post("/upload")
async def upload_invoice(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[-1].lower()
    temp_path = os.path.join(UPLOAD_DIR, f"temp{suffix}")
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        async with AsyncClient(base_url="http://localhost:8000") as client:
            with open(temp_path, "rb") as image_file:
                ocr_response = await client.post(
                    "/api/ocr",
                    files={"file": (file.filename, image_file, file.content_type)},
                )
            ocr_response.raise_for_status()
            ocr_result = ocr_response.json()["ocr_output"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR step failed: {e}")
        
    markdown_path = os.path.join(UPLOAD_DIR, "ocr_output.md")
    try:
        with open(markdown_path, "w", encoding="utf-8") as md_file:
            md_file.write(ocr_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write OCR result to markdown: {e}")
        
    # Read markdown and call /api/parse
    try:
        with open(markdown_path, "r", encoding="utf-8") as md_file:
            markdown_content = md_file.read()
    
        async with AsyncClient(base_url="http://localhost:8000") as client:
            parse_response = await client.post("/api/parse", json={"ocr_output": markdown_content})
            parse_response.raise_for_status()
            result = parse_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parse step failed: {e}")
        
    return result
