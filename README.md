# Ai-Agent-PDF-Buddy

A simple AI agent that reads multiple PDFs, stores their content using embeddings, and answers questions using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

* 📂 Load multiple PDFs
* ✂️ Chunk text for better retrieval
* 🧠 Local embeddings (no cost)
* ⚡ Fast similarity search using FAISS
* 🤖 Answer generation using Google Gemini API
* 📌 Source tracking (which PDF the answer came from)

---

## 🧠 Architecture

```
PDFs → Text Extraction → Chunking → Embeddings → FAISS
                                                ↓
                                           User Query
                                                ↓
                                       Retrieve Chunks
                                                ↓
                                         Gemini LLM
                                                ↓
                                           Final Answer
```

---

## 📁 Project Structure

```
project/
 ├── data/          # Add your PDF files here
 ├── app.py         # Main application
 ├── README.md
```

---

## ⚙️ Installation

```bash
pip install google-generativeai faiss-cpu pypdf sentence-transformers numpy
```

---

## 🔑 Setup API Key

Get your API key from Google AI Studio and set it in your code:

```python
genai.configure(api_key="YOUR_API_KEY")
```

---

## ▶️ Run the App

```bash
python app.py
```

You’ll see:

```
Loading PDFs...
Building index...
Ready! Ask questions.
```

---

## 💬 Example Usage

```
>> What is this document about?
>> Summarize the key points
>> What are the conclusions?
```

---

## ⚠️ Important Notes

* Works only with **text-based PDFs**
* Scanned PDFs (images) require OCR (not included)
* First run may be slow due to embedding generation
* Data is stored in memory (not persistent yet)

---

## 🧪 Tech Stack

* Google Gemini (LLM)
* Sentence Transformers (Embeddings)
* FAISS (Vector Database)
* PyPDF (PDF Parsing)

---

## 🚧 Limitations

* No UI (CLI-based)
* No persistent storage
* No chat memory
* Limited by Gemini free-tier quotas

---

## 🔥 Future Improvements

* Save/load FAISS index
* Add Streamlit or web UI
* Add chat history memory
* Improve chunking strategy
* Add OCR for scanned PDFs
* Deploy as API (FastAPI)

---

## 💡 How it Works (Simple)

1. PDFs are loaded and converted to text
2. Text is split into smaller chunks
3. Each chunk is converted into embeddings
4. Stored in FAISS for fast search
5. User asks a question
6. Relevant chunks are retrieved
7. Gemini generates answer using those chunks

---

## 🛑 Common Issues

### ❌ Model not found error

Use:

```
gemini-1.5-flash-latest
```

### ❌ No answer returned

* Check if PDFs are loaded
* Ensure text extraction is working

### ❌ Empty output

* PDF may be scanned (use OCR)

---

## 📌 Author

Built as a learning project for understanding RAG systems and LLM integration.

---

## ⭐ Final Note

This is a **minimal working RAG system**.
Focus on understanding the flow before adding complexity.

