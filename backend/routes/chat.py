from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, ChatResponse
from services.rag_pipeline import ask_question
 
router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        answer, sources = ask_question(request.session_id, request.question)
        return ChatResponse(
            answer=answer,
            sources=sources,
            session_id=request.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

