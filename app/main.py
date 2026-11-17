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
from app.summary_service import generate_summary, ensure_devanagari, has_urdu_script
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
    return {"version": "hindi-fix-v4"}

@app.post("/upload-audio")
def upload_audio(
    file: UploadFile = File(...),
    language: Optional[str] = Form("hi"),
    is_lyrics: bool = Form(True),
):
    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    received_language = language
    print("LANGUAGE RECEIVED:", repr(received_language))

    # Khali / auto / None ko Hindi maano
    if not language or language.strip().lower() in ("auto", "none", "null", "undefined"):
        language = "hi"
    language = language.strip().lower()

    text = transcribe_audio(file_path, language=language, is_lyrics=is_lyrics)

    if not text.strip():
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "transcript": "",
            "summary": ["No speech or lyrics detected (audio may be instrumental)"],
            "language_received": received_language,
            "language_used": language,
        }

    was_urdu = has_urdu_script(text)
    converted = False

    # Urdu script mile to Devanagari me convert karo (jab tak user ne explicitly "ur" na bheja ho)
    if was_urdu and language != "ur":
        text = ensure_devanagari(text)
        converted = not has_urdu_script(text)

    print("WAS_URDU:", was_urdu, "| CONVERTED:", converted)

    summary = generate_summary(text)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "transcript": text,
        "summary": summary,
        "language_received": received_language,
        "language_used": language,
        "was_urdu": was_urdu,
        "converted": converted,
    }