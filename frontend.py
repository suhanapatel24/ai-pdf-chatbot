import streamlit as st
from backend import extract_text_from_pdf, chunk_text, create_faiss_index, get_answer

st.set_page_config(page_title="LexiBot - AI PDF Chatbot", page_icon="📄", layout="wide")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("LexiBot - AI PDF Chatbot")
st.markdown("Upload PDFs, ask questions, and retrieve answers grounded in your documents.")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs",
    type=["pdf"],
    accept_multiple_files=True,
)

st.sidebar.markdown("### How it works")
st.sidebar.markdown(
    "1. Upload one or more PDFs\n"
    "2. LexiBot extracts and indexes the text\n"
    "3. Ask a question\n"
    "4. Review the answer and retrieved context"
)

if uploaded_files:
    with st.spinner("Processing PDFs..."):
        all_text = ""
        for uploaded_file in uploaded_files:
            extracted = extract_text_from_pdf(uploaded_file)
            if extracted.startswith("Error"):
                st.sidebar.error(extracted)
                continue
            all_text += extracted + "\n"

    if all_text.strip():
        chunks = chunk_text(all_text)
        vector_store = create_faiss_index(chunks)

        if vector_store:
            st.sidebar.success(f"Indexed {len(chunks)} text chunks.")
            query = st.text_input("Ask a question about your PDFs")

            if query:
                with st.spinner("Generating grounded response..."):
                    response, relevant_docs = get_answer(
                        vector_store, query, st.session_state.chat_history
                    )
                st.session_state.chat_history.append(
                    {"question": query, "answer": response}
                )
                st.subheader("AI Answer")
                st.write(response)

                if relevant_docs:
                    with st.expander("Retrieved document context"):
                        for index, doc in enumerate(relevant_docs, start=1):
                            st.markdown(f"**Context {index}**")
                            st.write(doc.page_content)

            if st.session_state.chat_history:
                st.subheader("Chat History")
                for chat in reversed(st.session_state.chat_history):
                    with st.expander(f"Q: {chat['question']}"):
                        st.write(chat["answer"])
        else:
            st.error("Could not create the FAISS index.")
    else:
        st.warning("No extractable text was found in the uploaded PDFs.")
else:
    st.info("Upload one or more text-based PDFs to get started.")
