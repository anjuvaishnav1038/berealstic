# from sentence_transformers import SentenceTransformer

# def create_embeddings(chunks):
#     model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
#     vectors = model.encode(chunks, show_progress_bar=True)
#     return vectors
from sentence_transformers import SentenceTransformer
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device set to use {device}")

from sentence_transformers import SentenceTransformer

def get_embedder():
    """Return a pre-trained embedding model."""
    return SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(embedder, texts):
    """Embed a list of texts into vector representations."""
    return embedder.encode(texts, show_progress_bar=True)


