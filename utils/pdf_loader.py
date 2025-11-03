# import fitz  # PyMuPDF
# import os

# def extract_text_from_pdfs(folder_path):
#     texts = []
#     for file in os.listdir(folder_path):
#         if file.endswith(".pdf"):
#             doc = fitz.open(os.path.join(folder_path, file))
#             text = ""
#             for page in doc:
#                 text += page.get_text()
#             texts.append(text)
#     return texts
from PyPDF2 import PdfReader
import os

def load_pdfs_from_folder(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            try:
                reader = PdfReader(os.path.join(folder_path, filename))
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                documents.append({"name": filename, "content": text})
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return documents

