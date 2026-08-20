import chromadb


class VectorRepository:

    def __init__(self, collection_name: str = "documents"):

        self.client = chromadb.PersistentClient(
            path="./chroma_data"
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_chunks(self, chunks, embeddings):

        ids = [
            f"chunk_{index}"
            for index in range(len(chunks))
        ]

        documents = [
            chunk.page_content
            for chunk in chunks
        ]

        metadatas = [
            chunk.metadata
            for chunk in chunks
        ]

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

        print(f"Added {len(chunks)} chunks to ChromaDB")

    def search(self, query_embedding, top_k=5):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results

    
    def get_all_chunks(self):

        return self.collection.get(
            include=["documents", "metadatas"]
        )


if __name__ == "__main__":

    repo = VectorRepository()

    data = repo.get_all_chunks()

    documents = data["documents"]
    metadatas = data["metadatas"]

    print(f"Total chunks: {len(documents)}")

    for i in range(min(10, len(documents))):

        print("\n" + "=" * 60)

        print(f"Chunk: {i + 1}")
        print(f"Page: {metadatas[i].get('page')}")
        print(f"Content:")
        print(documents[i][:500])            