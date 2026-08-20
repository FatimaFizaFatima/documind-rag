from pydantic import BaseModel
from datetime import datetime

class UploadResponse(BaseModel):

    filename : str
    total_pages : int
    total_chunks : int
    uploaded_at : datetime

class QueryRequest(BaseModel):
    question : str

class Source(BaseModel):
    filename : str
    page : int
    snippet : str

class QueryResponse(BaseModel):
    answer : str
    sources : list[Source]
