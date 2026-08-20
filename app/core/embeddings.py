from sentence_transformers import SentenceTransformer

def get_embeddings_model():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model


def generate_embeddings(chunks, model):
    texts = [chunk.page_content for chunk in chunks]
    embeddings = model.encode(texts)
    return embeddings