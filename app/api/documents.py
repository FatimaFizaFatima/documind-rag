from fastapi import UploadFile, File, APIRouter
from app.schemas.document import UploadResponse, QueryResponse, Source, QueryRequest
from app.service.ingestion_service import run_ingestion
import os
import shutil
from app.core.config import UPLOAD_DIR
from datetime import datetime


router = APIRouter()


@router.post("/documents/upload", response_model=UploadResponse)
def document_upload(file: UploadFile = File(...)):

    save_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks, embeddings, total_pages = run_ingestion(save_path)

    return UploadResponse(
        filename=file.filename,
        total_pages= total_pages,
        total_chunks= len(chunks),
        uploaded_at= datetime.utcnow()
    )    