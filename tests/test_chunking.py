from langchain_core.documents import Document
from app.core.chunking import chunk_documents   

def test_chunk_size_respected():
    sample_doc = [Document(page_content="A " * 300, metadata={})]
    chunks = chunk_documents(sample_doc, chunk_size=500, chunk_overlap=50)
    for chunk in chunks:
        assert len(chunk.page_content) <= 500
    print("PASSED: no chunk exceeds chunk_size")


def test_short_document_single_chunk():
    short_doc = [Document(page_content="Just one short sentence.", metadata={})]
    chunks = chunk_documents(short_doc, chunk_size=500, chunk_overlap=50)
    assert len(chunks) == 1
    print("PASSED: short document produces exactly 1 chunk")


def test_overlap_exists():
    long_doc = [Document(page_content="Sentence one. " * 100, metadata={})]
    chunks = chunk_documents(long_doc, chunk_size=500, chunk_overlap=50)
    assert len(chunks) > 1
    end_of_first = chunks[0].page_content[-30:]
    start_of_second = chunks[1].page_content[:100]
    assert end_of_first[:15] in start_of_second
    print("PASSED: overlap exists between chunks")


if __name__ == "__main__":
    test_chunk_size_respected()
    test_short_document_single_chunk()
    test_overlap_exists()