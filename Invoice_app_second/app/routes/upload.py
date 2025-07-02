# app/routes/upload.py

import os, shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
from httpx import AsyncClient

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

@router.post("/upload")
async def upload_invoice(request: Request, file: UploadFile = File(...), ):
    suffix = os.path.splitext(file.filename)[-1].lower()
    temp_path = os.path.join(UPLOAD_DIR, f"temp{suffix}")

    # Save file locally
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Call /ocr endpoint
    try:
        async with AsyncClient(app=request.app, base_url="http://app") as client:
            with open(temp_path, "rb") as image_file:
                ocr_response = await client.post("/api/ocr", files={"file": (file.filename, image_file, file.content_type)})
            ocr_response.raise_for_status()
            ocr_result = ocr_response.json()["ocr_output"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR step failed: {e}")

    # Call /parse endpoint
    try:
        async with AsyncClient(app=request.app, base_url="http://app") as client:
            parse_response = await client.post("/api/parse", json={"ocr_output": ocr_result})
            parse_response.raise_for_status()
            result = parse_response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parse step failed: {e}")

    return JSONResponse(content=result)
