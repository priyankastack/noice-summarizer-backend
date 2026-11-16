from fastapi import FastAPI, UploadFile, File
import os
import shutil

from app.whisper_service import transcribe_audio
from app.summary_service import generate_summary  
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"message": "Backend Running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload-audio")
def upload_audio(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = transcribe_audio(file_path)
    summary = generate_summary(text)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "transcript": text,
        "summary":summary
    }