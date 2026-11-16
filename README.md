# Python Backend - Voice Note Summariser

## Overview

This project is a FastAPI backend for the Voice Note Summariser application. It receives uploaded audio files, transcribes speech to text, and generates summaries using AI models.

## Tech Stack

* Python
* FastAPI
* Uvicorn
* Whisper (speech-to-text)
* Anthropic Claude API (summary generation)
* python-dotenv

## Features

* Audio file upload API
* Speech transcription
* AI-generated summaries
* CORS enabled for frontend integration
* Ready for deployment on Render

## Project Structure

```text
python-backend/
├── app/
│   ├── main.py
│   ├── whisper_service.py
│   └── summary_service.py
├── requirements.txt
├── .env
└── README.md
```

## Environment Variables

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your_api_key
ANTHROPIC_MODEL=claude-sonnet-4-5
```

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run Locally

```bash
uvicorn app.main:app --reload
```

Server runs on:

```text
http://127.0.0.1:8000
```

## API Endpoints

### Health Check

`GET /health`

### Upload Audio

`POST /upload-audio`

Form data:

* `file`: audio file

Response:

```json
{
  "transcript": "...",
  "summary": ["..."]
}
```

## Deployment (Render)

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Notes

* Use lightweight Whisper models for low-memory environments.
* Store secrets in platform environment variables, not in Git.
* Ensure frontend backend URL is configured correctly.
