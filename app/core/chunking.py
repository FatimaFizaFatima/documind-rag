from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(document, chunk_size=500, chunk_overlap=50):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap
    )

    chunker = splitter.split_documents(document)
    return chunker