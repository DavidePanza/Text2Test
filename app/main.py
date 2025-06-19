import streamlit as st
from utils import *
from main_IO import *
from download_questions import create_docx_from_data
from backend.raw_text_processing import *
from backend.chromadb_utils import *
import os
import sys
import logging


# Add the root folder (one level above 'app') to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# Configuration
configure_page()
initialise_session_state()
apply_style()

# add_sidebar_header()
st.sidebar.html("""
<div style='position: fixed; top: 10px; left: 20px; z-index: 999; padding: 10px;'>
    <h3>Menu</h3>
</div>
""")

# Initialize chromadb variables
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
model_path = "./chromadb_model"

# Set-up Logger
st.session_state.use_logger = True
if st.session_state.use_logger: 
    level = st.selectbox("Logging level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    logging.getLogger().setLevel(getattr(logging, level))

# Set default page if not specified
if "page" not in st.query_params:
    st.query_params.page = "main"

# Navigation handling
if st.query_params.page == "topic":
    st.switch_page("pages/2_topic_questions.py")
elif st.query_params.page == "chapter":
    st.switch_page("pages/1_chapter_questions.py")
elif st.query_params.page == "inspect":
    st.switch_page("pages/3_inspect_pdf.py")
else:
    # Welcome message
    st.title("Welcome to Text2Test!")
    st.divider()
    st.markdown("""
    Welcome! This app helps you transform your PDFs or texts into interactive study materials by generating meaningful questions.  
    You can either:

    - Generate questions based on specific topics or keywords
    - Generate questions from a selected chapter

    Start by uploading your PDF file, then choose your preferred way to generate questions using the options below.  
    Let’s make studying smarter and more engaging!
    """)
    st.divider()

    # Upload PDF file
    st.subheader("Upload your PDF file")
    upload_pdf()
    st.divider()

    # Check if PDF has changed or needs processing
    if st.session_state.get("pdf_changed") or (
        st.session_state.get("full_text") is None and 
        st.session_state.get("uploaded_pdf_bytes") is not None
    ):
        process_pdf()  # Extract text from PDF

        with st.spinner("Extracting information from the text..."):
            client, embedding_func = initialize_chromadb(EMBEDDING_MODEL)  
            whole_text_collection = initialize_collection(client, embedding_func, "whole_text_chunks")  
            update_collection(
                whole_text_collection, 
                st.session_state.get("full_text"), 
                max_words=200, 
                min_words=100, 
                overlap_sentences=3
            )
            st.session_state["pdf_changed"] = False  # Reset flag after processing

    try:
        uploaded_pdf_name = st.session_state.get('uploaded_pdf_name', None)
        if uploaded_pdf_name:
            st.info(f"Uploaded PDF: {uploaded_pdf_name}")
            debug_log(f"book title: {uploaded_pdf_name}")
        else:
            pass

        show_pdf_preview()

    except Exception as e:
        debug_log(f"Error displaying PDF info or preview: {e}")

    # Main content buttons
    st.subheader("Generate Questions")
    st.write("Please choose an option to generate questions:")
    breaks(1)  
    cols = st.columns(2)
    st.html("""
    <style>
    div.stButton {
        display: flex;
        justify-content: center;
        margin: 10px 0;
    }

    div.stButton > button:first-child {
        width: 80%;
        padding: 40px 0;
        background-color: #f0f0f0 !important;
        border: none !important;
        border-radius: 10px !important;
        color: #333 !important;
        font-family: 'Work Sans', sans-serif !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }

    /* Target the button text directly */
    div.stButton > button:first-child p,
    div.stButton > button:first-child span,
    div.stButton > button:first-child div,
    div.stButton > button:first-child {
        font-size: 24px !important;
        line-height: 1.2 !important;
    }

    div.stButton > button:first-child:hover {
        background-color: #e0e0e0 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    """)

    with cols[0]:
        if st.button("Generate Questions on a Topic", key="main_topic"):
            st.query_params.page = "topic"
            st.rerun()
    with cols[1]:
        if st.button("Generate Questions from a Chapter", key="main_chapter"):
            st.query_params.page = "chapter"
            st.rerun()

    if st.session_state.get('questions_to_download'): 
        with st.sidebar:
            st.markdown("---")  # Divider
            st.markdown("**Download Questions**")  # Spacing

            docx_file = create_docx_from_data(st.session_state.get('questions_to_download', {}))

            st.download_button(
                label="📄 Download as Word (.docx)",
                data=docx_file,
                file_name="questions.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                on_click="ignore"
            )
    else:
        with st.sidebar:
            st.markdown("---")
