from app.core.embeddings import get_embeddings_model
from app.repositories.vector_repo import VectorRepository
from app.core.llm_client import generate_answer
from pathlib import Path

def retrieve_relevant_chunks(question : str, top_k : int = 3):

    model = get_embeddings_model()
    query_embedding = model.encode([question])[0]

    repo = VectorRepository()
    results = repo.search(query_embedding=query_embedding, top_k=top_k)
    return results


def build_rag_prompt(question : str, retrieved_chunks : dict)->str:

    context_texts = retrieved_chunks["documents"][0]
    context = "\n\n".join(context_texts)

    prompt = f"""You are a helpful assistant who answer the queries based only on the provided context.

    Context:
    \"\"\"
    {context}
    \"\"\"

    Question: {question}

    Instructions:
    - Answer using only the information in the context above.
    - If the context does not contain enough information to answer, say so clearly.
    - Keep your answer concise and directly relevant to the question.

    Answer:
    """

    return prompt



def build_sources(retrieved_chunks):

    metadatas = retrieved_chunks["metadatas"][0]
    documents = retrieved_chunks["documents"][0]

    sources = []

    for metadata, document in zip(metadatas, documents):

        source_path = metadata.get("source", "")

        source = {
            "filename": Path(source_path).name,
            "page": metadata.get("page", 0) + 1,
            "snippet": document[:300]
        }

        sources.append(source)

    return sources

def answer_question(question: str, top_k: int = 3, distance_threshold: float = 1.1):
    retrieved_chunks = retrieve_relevant_chunks(question, top_k)

    best_distance = retrieved_chunks["distances"][0][0]
    if best_distance > distance_threshold:
        return {
            "answer": "I don't have enough relevant information in the uploaded document to answer this question.",
            "sources": []
        }

    prompt = build_rag_prompt(question, retrieved_chunks)
    answer = generate_answer(prompt)
    sources = build_sources(retrieved_chunks)

    return {"answer": answer, "sources": sources}

# if __name__ == "__main__":

#     question = "What does the article examine about Studio Ghibli?"

#     result = answer_question(question)

#     print("\nANSWER:")
#     print(result["answer"])

#     print("\nSOURCES:")

#     for source in result["sources"]:
#         print(source)

#     print("\nRETRIEVED CHUNKS:")

#     retrieved_chunks = retrieve_relevant_chunks(
#         question,
#         top_k=3
#     )

#     documents = retrieved_chunks["documents"][0]
#     metadatas = retrieved_chunks["metadatas"][0]
#     distances = retrieved_chunks["distances"][0]

#     for i, (document, metadata, distance) in enumerate(
#         zip(documents, metadatas, distances)
#     ):

#         print(f"\n--- Chunk {i + 1} ---")
#         print(f"Page: {metadata.get('page')}")
#         print(f"Distance: {distance}")
#         print(f"Content: {document[:500]}")