from app.service.ingestion_service import run_ingestion
from app.repositories.document_repo import DocumentRepository


def test_full_ingestion_and_storage():
    chunks, embeddings, repo = run_ingestion("D:/RAG Pipeline Project/documind-rag/data/uploads/sample.pdf")

    results = repo.search(embeddings[0], top_k=3)
    print("Search results:", results["documents"])
    assert len(results["documents"][0]) > 0

    doc_repo = DocumentRepository()
    docs = doc_repo.get_all_documents()
    assert len(docs) > 0
    print(f"SQLite has {len(docs)} document(s) recorded")


if __name__ == "__main__":
    test_full_ingestion_and_storage()