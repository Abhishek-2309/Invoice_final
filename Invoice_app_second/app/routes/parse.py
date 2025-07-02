# app/routes/parse.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.invoice_parser import process_invoice
from app.services.llm_engine import llm

router = APIRouter()

class ParseInput(BaseModel):
    ocr_output: str

@router.post("/parse")
async def parse_endpoint(data: ParseInput):
    try:
        print(data.ocr_output)
        result = process_invoice(data.ocr_output, llm)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse invoice: {e}")
