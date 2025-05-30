import streamlit as st
import chromadb
from app.utils import *
from app.main_IO import *
from app.download_questions import create_docx_from_data
from app.pages.utils_chapter.display_questions import *
from app.pages.utils_chapter.chapter_selection import select_num_questions
from app.backend.chunks_processing import query_collection
from app.backend.messages_templates import book_prompt
from app.backend.runpod_client import run_prompt, clean_and_parse_json


# Initialise
apply_style()

# add_sidebar_header()
st.sidebar.html("""
<div style='position: fixed; top: 10px; left: 20px; z-index: 999; padding: 10px;'>
    <h3>Menu</h3>
</div>
""")

show_pdf_preview()
st.title("Generate Questions on a Topic")
st.divider()
st.write("""Here, you can generate questions based on a specific topic.  
        You can enter a topic or keyword, and the app will generate questions based on the content of the uploaded PDF.""")

breaks(1)

# Set up logger
if st.session_state.use_logger: 
    level = st.selectbox("Logging level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    logging.getLogger().setLevel(getattr(logging, level))

if st.session_state.get("full_text", None) is not None:
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
    st.subheader("Enter a Topic or Keyword")
    query = st.text_input("Enter your query:")
    col1, _ = st.columns([2, 6])
    with col1:
        num_questions = select_num_questions()
    breaks(1)
    submitted = st.form_submit_button("Submit")

    if submitted and query:
        with st.spinner("Generating questions..."):
            # Generate questions based on the query
            query_context = query_collection(whole_text_collection, query=query, nresults=3, context_multiplier=2)
            prompt = book_prompt(query_context, num_questions=num_questions, user_query=query)
            questions_json = run_prompt(prompt)
            st.session_state.questions_dict_topic = clean_and_parse_json(questions_json)
            st.session_state['query'] = query
            st.session_state['questions_ready_topic'] = True

if st.session_state.get("questions_ready_topic"):
    breaks(2)
    st.subheader("Generated Questions")
    st.divider()
    debug_log(f"Generated questions: {st.session_state.get('questions_dict_topic', 'None')}")

    # Visualize generated questions and store them
    show_questions(st.session_state['questions_dict_topic'])
    breaks(1)
    show_download_controls(st.session_state.get('query'), st.session_state.get('questions_dict_topic', 'None'))
    debug_show_selected_questions()

    with st.sidebar:
        st.divider()  # Divider
        st.markdown("**Download Questions**")  # Spacing

        docx_file = create_docx_from_data(st.session_state.get('questions_to_download', {}))

        st.download_button(
            label="📄 Download as Word (.docx)",
            data=docx_file,
            file_name="questions.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            on_click="ignore"
        )




        # query_context = query_collection(whole_text_collection, query=query, nresults=3, context_multiplier=2)
        # out3 = book_prompt(query_context, num_questions=3, user_query=query)
        # questions = run_prompt(out)


# use https://docs.streamlit.io/develop/api-reference/chat/st.chat_input
# or https://docs.streamlit.io/develop/api-reference/widgets/st.text_input