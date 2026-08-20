from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

from app.core.cleaning import clean_data
from app.core.chunking import chunk_documents
from app.core.embeddings import generate_embeddings, get_embeddings_model
from app.repositories.document_repo import DocumentRepository
from app.repositories.vector_repo import VectorRepository


def run_ingestion(file_path: str):

    loader = PyPDFLoader(file_path=file_path)
    documents = loader.load()

    print(f"Loaded {len(documents)} pages")

    for document in documents:
        document.page_content = clean_data(document.page_content)

    print("Text cleaning completed")

    chunks = chunk_documents(
        documents,
        chunk_size=500,
        chunk_overlap=50
    )

    print(f"Created {len(chunks)} chunks")

    model = get_embeddings_model()
    embeddings = generate_embeddings(chunks, model)

    print(f"Generated {len(embeddings)} embeddings")

    vector_repo = VectorRepository()
    vector_repo.add_chunks(chunks, embeddings)

    print("Chunks and embeddings stored in ChromaDB")

    document_repo = DocumentRepository()

    filename = Path(file_path).name

    document_repo.add_document(
        filename=filename,
        source_path=file_path,
        total_pages=len(documents),
        total_chunks=len(chunks)
    )

    print("Document metadata saved to SQLite")

    print(
        f"Ingestion complete: "
        f"{len(documents)} pages → "
        f"{len(chunks)} chunks → "
        f"{len(embeddings)} embeddings"
    )

    document_repo.close()

    return chunks, embeddings, len(documents)


if __name__ == "__main__":
    run_ingestion(
        "D:/RAG Pipeline Project/documind-rag/data/uploads/sample.pdf"
    )