# def split_text(texts, chunk_size=800, overlap=100):
#     chunks = []
#     for text in texts:
#         start = 0
#         while start < len(text):
#             end = start + chunk_size
#             chunks.append(text[start:end])
#             start += chunk_size - overlap
#     return chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(texts, chunk_size=800, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = []
    for text in texts:
        docs.extend(splitter.split_text(text))
    return docs


