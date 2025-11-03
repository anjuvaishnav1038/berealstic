
import os
from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from utils.vector_store import create_faiss_index, search_vectors
from utils.web_search_agent import web_search
from utils.image_ocr import extract_text_from_image
from utils.vector_store import create_faiss_index, search_vectors
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
index = None
texts = []

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def extract_text_from_image(img_path):
    img = Image.open(img_path)
    text = pytesseract.image_to_string(img)
    return text


def build_knowledge_base(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext in [".png", ".jpg", ".jpeg"]:
        text = extract_text_from_image(file_path)
    else:
        raise ValueError("Unsupported file format")

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = splitter.split_text(text)

    # Build FAISS index
    index = create_faiss_index(texts)

    return index, texts


def answer_query(query, index, texts):
    matched_chunks = search_vectors(query, index)
    # Just returning top relevant chunks
    return matched_chunks


def load_llm():
    """
    Loads FLAN-T5 model for text generation/QA.
    Runs on GPU if available.
    """
    model_name = "google/flan-t5-large"
    device = 0 if torch.cuda.is_available() else -1
    print(f" Loading model {model_name} on {'GPU' if device == 0 else 'CPU'}")

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if device == 0 else torch.float32
    )

    llm_pipe = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        device=device,
        max_new_tokens=512
    )

    return llm_pipe


def answer_query(query, index, texts):
    """
    Uses the RAG pipeline: first search PDFs via FAISS, then LLM.
    If not found in PDFs, fallback to web search.
    """
    if not index or not texts:
        print(" Knowledge base empty, using web search.")
        return web_search(query)

    # Step 1: Retrieve relevant chunks
    context_chunks = search_vectors(query, top_k=3)
    context = "\n".join(context_chunks)

    # Step 2: Generate answer using LLM
    llm = load_llm()
    prompt = f"""
    You are a helpful assistant. Answer based on the context below.
    If the context doesn’t contain the answer, say “Not found in context.”
    
    Context:
    {context}
    
    Question: {query}
    Answer:
    """

    result = llm(prompt)[0]["generated_text"].strip()

    # Step 3: If not found in PDF, fallback to web
    if "not found" in result.lower() or len(result) < 15:
        print(" Falling back to web search...")
        return web_search(query)

    return result
