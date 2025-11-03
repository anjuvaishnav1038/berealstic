

from fastapi import FastAPI, UploadFile, File, Query
from utils.rag_pipeline import build_knowledge_base, answer_query
from fastapi import FastAPI, File, UploadFile
from typing import List
import os
import fitz  # PyMuPDF for PDF
from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import pytesseract
from fastapi import FastAPI, Query
from utils.rag_pipeline import build_knowledge_base, answer_query

index = None
texts = []
app = FastAPI()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# store index and texts persistently in app.state
app.state.index = None
app.state.texts = []


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file locally
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Build FAISS index and texts (PDF or Image)
    index, texts = build_knowledge_base(file_path)

    # Store in app state (shared memory)
    app.state.index = index
    app.state.texts = texts

    return {
        "message": " File uploaded and indexed successfully.",
        "filename": file.filename,
        "chunks": len(texts)
    }


@app.get("/ask/")
async def ask_question(q: str = Query(...)):
    if app.state.index is None or not app.state.texts:
        return {"error": "Please upload a PDF or image first."}

    answer = answer_query(q, app.state.index, app.state.texts)
    return {"response": answer}

