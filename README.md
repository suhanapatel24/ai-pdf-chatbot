# LexiBot - AI PDF Chatbot

A multi-document PDF question-answering application built around the original Streamlit frontend project.

The supplied frontend supports uploading multiple PDFs, extracting and chunking their text, building a FAISS vector index, asking questions, and retaining chat history. The original Python source for the backend was not included with the recovered project files; only a compiled Python 3.9 backend artifact was supplied. This repository therefore preserves the frontend behavior and provides a clean reconstruction of the backend interface it imports.

## Features

- Upload multiple text-based PDF documents
- Extract text page by page
- Split documents into overlapping semantic chunks
- Create a FAISS vector index
- Retrieve relevant document chunks for each question
- Generate answers grounded in retrieved PDF context
- Maintain Streamlit chat history
- Display source excerpts used for retrieval

## Architecture

```text
PDF uploads
    |
    v
PyPDF text extraction
    |
    v
Recursive text chunking
    |
    v
Sentence Transformer embeddings
    |
    v
FAISS vector store
    |
    +--> similarity retrieval --> context
                               |
question ----------------------+
                               v
                         LLM answer
                               |
                               v
                      Streamlit chat UI
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run frontend.py
```

For AI-generated answers, set an OpenAI API key in your environment:

```bash
export OPENAI_API_KEY="your-key"
```

Do not commit API keys or other credentials.

## Important source note

`frontend.py` is based on the uploaded project source. `backend.py` is a reconstruction matching the four functions imported by that frontend:

- `extract_text_from_pdf`
- `chunk_text`
- `create_faiss_index`
- `get_answer`

The compiled `backend.cpython-39.pyc` was not treated as editable source code.

## Limitations

- Scanned/image-only PDFs require OCR and are not handled by the current extractor.
- Answer quality depends on PDF text quality, retrieval quality, and the configured language model.
- Retrieved context is supplied to the model with instructions to avoid inventing unsupported answers.
