from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.services.gemini import ask_medical_question

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    text: str

class ChatRequest(BaseModel):
    message: str
    file_uri: Optional[str] = None
    history: Optional[List[ChatMessage]] = None

@router.post("/")
async def chat_with_ai(request: ChatRequest):
    if not request.message:
        raise HTTPException(status_code=400, detail="Message is required")
        
    try:
        ai_response = ask_medical_question(request.message, request.file_uri, request.history)
        return {"response": ai_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")
