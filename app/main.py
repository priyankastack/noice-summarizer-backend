# from fastapi import FastAPI, UploadFile, File, Form
# import os
# import shutil
# from typing import Optional

# from app.whisper_service import transcribe_audio
# from app.summary_service import generate_summary  
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# @app.get("/")
# def home():
#     return {"message": "Backend Running"}

# @app.get("/health")
# def health():
#     return {"status": "ok"}

# @app.post("/upload-audio")
# def upload_audio(
#     file: UploadFile = File(...),
#     language: Optional[str] = Form("hi"),  # default Hindi, auto-detect me Urdu script aa jati hai
#     is_lyrics: bool = Form(True),
# ):
#     os.makedirs("uploads", exist_ok=True)

#     file_path = f"uploads/{file.filename}"

#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     text = transcribe_audio(file_path, language=language or None, is_lyrics=is_lyrics)

#     if not text.strip():
#         return {
#             "message": "File uploaded successfully",
#             "filename": file.filename,
#             "transcript": "",
#             "summary": ["No speech or lyrics detected (audio may be instrumental)"],
#         }

#     summary = generate_summary(text)

#     return {
#         "message": "File uploaded successfully",
#         "filename": file.filename,
#         "transcript": text,
#         "summary": summary
#     }





from fastapi import FastAPI, UploadFile, File, Form
import os
import shutil
from typing import Optional

from app.whisper_service import transcribe_audio
from app.summary_service import generate_summary, ensure_devanagari
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

@app.get("/version")
def version():
    # Live pe naya code chal raha hai ya nahi, ye isse pata chalega
    return {"version": "hindi-fix-v3"}

@app.post("/upload-audio")
def upload_audio(
    file: UploadFile = File(...),
    language: Optional[str] = Form("hi"),  # default Hindi, auto-detect me Urdu script aa jati hai
    is_lyrics: bool = Form(True),
):
    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("LANGUAGE RECEIVED:", repr(language))

    text = transcribe_audio(file_path, language=language or None, is_lyrics=is_lyrics)

    if not text.strip():
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "transcript": "",
            "summary": ["No speech or lyrics detected (audio may be instrumental)"],
            "language_used": language,
        }

    # Urdu script aayi to Devanagari me convert karo (sirf Hindi selected ho tab)
    if language == "hi":
        text = ensure_devanagari(text)

    summary = generate_summary(text)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "transcript": text,
        "summary": summary,
        "language_used": language,
    }