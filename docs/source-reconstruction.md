# Source Reconstruction Note

The uploaded project included a readable `frontend.py` and a compiled `backend.cpython-39.pyc`, but not the original `backend.py`.

The frontend explicitly imports four backend functions:

1. `extract_text_from_pdf`
2. `chunk_text`
3. `create_faiss_index`
4. `get_answer`

It then uses them in this order: extract all uploaded PDF text, split the combined text into chunks, build a FAISS index, and retrieve an answer plus relevant documents for each user query.

The `backend.py` in this repository is a clean implementation of that observed interface. It should not be interpreted as a byte-for-byte recovery of the missing original backend source.
