import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def extract_text_from_pdf(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        pages = []
        for page in reader.pages:
            text = page.extract_text() or ""
            if text.strip():
                pages.append(text)
        return "\n".join(pages)
    except Exception as exc:
        return f"Error extracting PDF text: {exc}"

def chunk_text(text, chunk_size=1000, chunk_overlap=150):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text(text)

def create_faiss_index(chunks):
    if not chunks:
        return None
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return FAISS.from_texts(chunks, embedding=embeddings)

def _format_history(chat_history, max_turns=4):
    recent = chat_history[-max_turns:]
    return "\n".join(
        f"User: {item['question']}\nAssistant: {item['answer']}"
        for item in recent
    )

def get_answer(vector_store, query, chat_history=None, k=4):
    relevant_docs = vector_store.similarity_search(query, k=k)
    context = "\n\n---\n\n".join(doc.page_content for doc in relevant_docs)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        fallback = (
            "OPENAI_API_KEY is not configured. The most relevant document context is:\n\n"
            + context[:4000]
        )
        return fallback, relevant_docs

    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    history = _format_history(chat_history or [])

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
        instructions=(
            "Answer using only the supplied PDF context. "
            "If the context does not support the answer, say that the uploaded documents "
            "do not contain enough information. Do not invent citations or facts."
        ),
        input=(
            f"Recent conversation:\n{history}\n\n"
            f"Retrieved PDF context:\n{context}\n\n"
            f"Question: {query}"
        ),
    )
    return response.output_text, relevant_docs
