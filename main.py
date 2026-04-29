import os
import numpy as np
import faiss
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# -----------------------------
# CONFIG
# -----------------------------
PDF_FOLDER = "data"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K = 4

# Gemini setup
genai.configure(api_key="Add you api key")
llm = genai.GenerativeModel("gemini-2.5-flash")
for m in genai.list_models():
    print(m.name)

# Embedding model (local, FREE)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# PDF → TEXT
# -----------------------------
def load_pdfs(folder):
    documents = []
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            reader = PdfReader(os.path.join(folder, file))
            text = ""
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text()
            documents.append((file, text))
    return documents

# -----------------------------
# CHUNKING
# -----------------------------
def chunk_text(text):
    chunks = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]
        chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks

# -----------------------------
# BUILD VECTOR DB
# -----------------------------
def build_index(docs):
    texts = []
    metadata = []

    for filename, text in docs:
        chunks = chunk_text(text)
        for chunk in chunks:
            texts.append(chunk)
            metadata.append({"source": filename})

    embeddings = embed_model.encode(texts)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    return index, texts, metadata

# -----------------------------
# RETRIEVE
# -----------------------------
def retrieve(query, index, texts, metadata):
    query_embedding = embed_model.encode([query])
    distances, indices = index.search(np.array(query_embedding), TOP_K)

    results = []
    for i in indices[0]:
        results.append((texts[i], metadata[i]))

    return results

# -----------------------------
# GENERATE ANSWER (RAG)
# -----------------------------
def ask(query, index, texts, metadata):
    retrieved = retrieve(query, index, texts, metadata)

    context = "\n\n".join([r[0] for r in retrieved])

    prompt = f"""
You are a helpful AI. Answer ONLY from the context below.

Context:
{context}

Question:
{query}

If answer not found, say "Not found in documents".
"""

    response = llm.generate_content(prompt)

    sources = list(set([r[1]["source"] for r in retrieved]))

    return response.text, sources

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    print("Loading PDFs...")
    docs = load_pdfs(PDF_FOLDER)

    print("Building index...")
    index, texts, metadata = build_index(docs)

    print("Ready! Ask questions.\n")

    while True:
        query = input(">> ")
        if query.lower() == "exit":
            break

        answer, sources = ask(query, index, texts, metadata)

        print("\nAnswer:\n", answer)
        print("\nSources:", sources)
        print("\n" + "-"*50)
