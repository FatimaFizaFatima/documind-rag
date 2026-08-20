from fastapi import FastAPI
from app.api import documents 
from app.api import routes_query

app = FastAPI()


app.include_router(documents.router)
app.include_router(routes_query.router)