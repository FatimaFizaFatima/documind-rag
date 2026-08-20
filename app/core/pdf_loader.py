from langchain_community.document_loaders import PyPDFLoader
from app.core.cleaning import clean_data
from app.core.chunking import chunk_documents
from app.core.embeddings import get_embeddings_model, generate_embeddings


pdf_loader = PyPDFLoader(
    file_path="D:/RAG Pipeline Project/documind-rag/data/uploads/sample.pdf"
)

pdf_document = pdf_loader.load()


print(f"The total documents are: {len(pdf_document)}")


for index, doc in enumerate(pdf_document[:3]):

    print(f"--------Page {index+1}-----------")
    print("=" *50)
    print(f"The content {doc.page_content[:300]}")
    print("=" *50)
    print(f"The metadata {doc.metadata}")


