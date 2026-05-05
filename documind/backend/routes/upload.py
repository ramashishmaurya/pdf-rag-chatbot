from fastapi import APIRouter, UploadFile, File, Form
from services.document_loader import load_and_split
from services.vector_store import add_documents

router = APIRouter()

@router.post("/upload")
async def upload_document(
    session_id: str = Form(...),
    file: UploadFile = File(...)
):
    content = await file.read()
    documents = load_and_split(content, file.filename)
    add_documents(session_id, documents)
    
    return {
        "message": f"✅ '{file.filename}' uploaded successfully!",
        "chunks": len(documents),
        "session_id": session_id
    }