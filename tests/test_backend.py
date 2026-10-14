from backend import chunk_text

def test_chunk_text_returns_chunks():
    text = ("Cloud computing and Kubernetes. " * 200).strip()
    chunks = chunk_text(text, chunk_size=250, chunk_overlap=25)
    assert len(chunks) > 1
    assert all(chunk.strip() for chunk in chunks)

def test_empty_text():
    assert chunk_text("") == []
