import streamlit as st
from utils import *
from main_IO import *
from backend.raw_text_processing import *
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
    st.title("Welcome to Test2Test!")
    st.write("This app helps you generate questions from text documents or specific topics.")

    # Upload PDF file
    upload_pdf()

    if st.session_state.get("uploaded_pdf_bytes") is not None and st.session_state.get("full_text") is None:
        process_pdf() # maybe combine this with the upload_pdf function
        st.session_state["pages_data_infos"] = st.session_state["pages_data_infos"][st.session_state["chapters_starting_page"]:]

    try:
        st.info(st.session_state['uploaded_pdf_name'])      
        st.write(f'{st.session_state["full_text"][:200]}') # remove this
        show_pdf_preview()
    except:
        pass
    
    breaks(2)

    # Main content buttons
    st.write("Please choose an option to generate questions:")
    cols = st.columns(2)
    st.html("""
    <style>
    div.stButton > button:first-child {
        width: 100%;
        padding: 30px 0;
        font-size: 20px;
        background-color: #cce5ff;
        border-radius: 10px;
        border: 2px solid #339af0;
    }
    div.stButton > button:first-child:hover {
        background-color: #99ccff;
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




txt = st.text_area(
    "",
    "Text to analyze It was the best of times, it was the worst of times, it was the age of "
    "wisdom, it was the age of fool")

st.write(f"You wrote {len(txt)} characters.")