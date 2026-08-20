from fastapi import APIRouter
from app.schemas.document import QueryRequest, QueryResponse
from app.service.rag_service import answer_question

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    result = answer_question(request.question)
    return QueryResponse(**result)