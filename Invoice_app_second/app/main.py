from fastapi import FastAPI
from app.routes import ocr, parse, upload

app = FastAPI()

app.include_router(ocr.router, prefix="/api")
app.include_router(parse.router, prefix="/api")
app.include_router(upload.router, prefix="/api")

@app.get("/")
def root():
    return {"status": "FastAPI invoice app running"}

