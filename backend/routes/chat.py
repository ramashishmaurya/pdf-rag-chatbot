from fastapi import APIRouter
from models.schemas import ChatRequest, ChatResponse
from services.rag_pipeline import ask_question

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    answer, sources = ask_question(request.session_id, request.question)
    return ChatResponse(
        answer=answer,
        sources=sources,
        session_id=request.session_id
    )