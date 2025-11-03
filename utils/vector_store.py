from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import torch
import os

device = "cuda" if torch.cuda.is_available() else "cpu"
embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device=device)

index = None
chunks = []

def create_faiss_index(text_chunks):
    global index, chunks
    embeddings = embedding_model.encode(text_chunks, convert_to_numpy=True, show_progress_bar=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    chunks = text_chunks
    return f" FAISS index built with {len(text_chunks)} chunks."

def search_vectors(query, top_k=3):
    if index is None:
        return []
    query_emb = embedding_model.encode([query], convert_to_numpy=True)
    D, I = index.search(query_emb, top_k)
    return [chunks[i] for i in I[0]]

def save_faiss_index(path="vector_store/faiss_index.index"):
    if index:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        faiss.write_index(index, path)

def load_faiss_index(path="vector_store/faiss_index.index"):
    global index
    if os.path.exists(path):
        index = faiss.read_index(path)
        return index
    return None
