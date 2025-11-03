         ┌────────────────────────────┐
         │        User Interface      │
         │ (Postman / Frontend App)   │
         └──────────────┬─────────────┘
                        │
                        ▼
         ┌────────────────────────────┐
         │         FastAPI Router      │
         │  (/upload, /ask endpoints)  │
         └──────────────┬─────────────┘
                        │
                        ▼
         ┌────────────────────────────┐
         │     Multi-Modal Processor  │
         │  (PDF Loader + OCR Engine) │
         └──────────────┬─────────────┘
                        │
                        ▼
         ┌────────────────────────────┐
         │     Text Splitter + Embedder│
         │ (Sentence/Chunk generation) │
         └──────────────┬─────────────┘
                        │
                        ▼
         ┌────────────────────────────┐
         │      Vector Store (FAISS)  │
         │  (Stores embeddings)       │
         └──────────────┬─────────────┘
                        │
                        ▼
         ┌────────────────────────────┐
         │      Query + Generator     │
         │ (LLM-based response)       │
         └────────────────────────────┘
