"""
main.py
-------
FastAPI backend for the Financial Report Analyst AI Agent.

Exposes a small REST API that a React (or any) frontend can call:

    POST /api/upload   - upload a PDF, process it, build the vector index
    POST /api/ask       - ask a question about the currently loaded report
    POST /api/reset      - clear conversation memory (keeps the report loaded)
    GET  /api/status     - check whether a report is currently loaded

Run with:
    uvicorn main:app --reload --port 8000
"""

import os
import shutil
import uuid

from fastapi import FastAPI, File , UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.agent import FinancialReportAgent
from src.config import REPORTS_DIR

app = FastAPI(title="Financial Report Analyst API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = FinancialReportAgent()
state = {"report_loaded":False,"filename":None,"num_chunks":0}


class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str

class UploadResponse(BaseModel):
    filename: str
    num_chunks:int
    message: str

class StatusResponse(BaseModel):
    report_loaded: bool
    filename: str | None
    num_chunks: int

@app.get("/api/status",response_model=StatusResponse)
def get_status():
    return StatusResponse(
        report_loaded=state["report_loaded"],
        filename=state["filename"],
        num_chunks=state["num_chunks"],
        )

@app.post("/api/upload",response_model=UploadResponse)
async def upload_report(file:UploadFile=File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400,detail="Only PDF files are supported.")
    
    os.makedirs(REPORTS_DIR,exist_ok=True)
    safe_name = f"{uuid.uuid4().hex[:8]}_{file.filename}"
    save_path = os.path.join(REPORTS_DIR,safe_name)

    try:
        with open(save_path,"wb") as f:
            shutil.copyfileobj(file.file,f)
    finally:
        file.file.close()
    
    try:
        num_chunks = agent.load_report(save_path)
    except Exception as e:
        raise HTTPException(status_code=422,detail=f"Failed to process PDF: {e}")
    
    state["report_loaded"] = True
    state["filename"] = file.filename
    state["num_chunks"] = num_chunks

    return UploadResponse(
        filename = file.filename,
        num_chunks = num_chunks,
        message=f"Indexed {num_chunks} chunks from {file.filename}.",
    )

@app.post("/api/ask",response_model=AskResponse)
def ask_question(payload:AskRequest):
    if not state["report_loaded"]:
        raise HTTPException(
            status_code=400,
            detail="No reportloaded yet. Upload a PDF via/api/upload first.",

        )
    if not payload.question or not payload.question.strip():
        raise HTTPException(status_code=400,detail="Question must not be empty.")
    
    try:
        answer = agent.ask(payload.question)
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Agent error:{e}")
    
    return AskResponse(answer=answer)

@app.post("/api/reset")
def reset_memory():
    agent.reset_memory()
    return {"message":"Conversation memory cleared ."}

@app.get("/")
def root():
    return{
        "service": "Financial Report Analyst API",
        "docs":"/docs",
        "endpoints":["/api/upload","/api/ask","/api/reset","/api/status"],
    }