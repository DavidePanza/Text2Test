import streamlit as st
import chromadb
from app.utils import *
from app.main_IO import *
from app.pages.utils_chapter.display_questions import *
from app.pages.utils_chapter.download_questions import create_docx_from_data


# Initialise
apply_style()
show_pdf_preview()
st.title("Generate Questions on a Topic")
st.write("Here, you can generate questions based on a specific topic.")

# Set up logger
level = st.selectbox("Logging level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
logging.getLogger().setLevel(getattr(logging, level))

if st.session_state['uploaded_pdf_bytes'] is not None:
    st.write("You have uploaded a PDF file. You can now generate questions based on the content of the PDF.")

client = chromadb.Client()  # Use same client init/config
whole_text_collection = client.get_collection("whole_text_chunks")
debug_log(f"Collection name: {whole_text_collection.name}")
debug_log(f"Number of documents: {whole_text_collection.count()}")
results = whole_text_collection.get(limit=1)

documents = results['documents']  # List of text chunks
metadatas = results['metadatas']  # List of metadata dicts, e.g. chunk indexes

for i, (doc, meta) in enumerate(zip(documents, metadatas)):
    debug_log(f"Chunk {i}:")
    debug_log(doc)
    debug_log(f"Metadata: {meta}")


with st.form("query_form"):
    query = st.text_input("Enter your query:")
    submitted = st.form_submit_button("Submit")

if submitted and query:
    st.write(f"You asked: {query}")

    query_context = query_collection(whole_text_collection, query=query, nresults=3, context_multiplier=2)
    out3 = book_prompt(query_context, num_questions=3, user_query=query)
    questions = run_prompt(out)

# use https://docs.streamlit.io/develop/api-reference/chat/st.chat_input
# or https://docs.streamlit.io/develop/api-reference/widgets/st.text_input