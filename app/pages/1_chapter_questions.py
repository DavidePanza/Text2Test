import streamlit as st
import json
from app.utils import *
from app.main_IO import *
from app.pages.ui_utils.page1_utils import *
from app.backend.raw_text_processing import *
from app.backend.toc_parser import extract_chapters_from_toc
from app.backend.text_processing import chapters_chunking


st.title("Generate Questions from a Chapter")
st.write("Here, you can generate questions based on a specific chapter.")

# if st.button("Back to Main"):
#     st.switch_page("main.py")

# if st.session_state.get("uploaded_pdf_bytes") is None:
#     st.warning("Please upload a PDF file to generate questions from a chapter.")
# else:
#     pass

show_pdf_preview()
display_scrollable_pages()
page_range_selector()

if st.session_state['toc_page_range'] is not None:
    st.write(f"Selected page range: {st.session_state['toc_page_range'][0] + 1} to {st.session_state['toc_page_range'][1] + 1}")

    extract_pages_range(st.session_state['toc_page_range'])
    st.write(f"Table of Contents (TOC): {st.session_state.get('toc')[:200]}")

if st.session_state['toc'] is not None:
    with st.spinner("Extracting chapters from TOC..."):
        extract_chapters_from_toc(st.session_state['toc'])
        st.success("Chapters extracted successfully.")

try:
    st.write(st.session_state['chapters_dict'][0])
    st.write(st.session_state['pages_data_infos'][0])
except:
    pass

extract_chapters(st.session_state['chapters_dict'], st.session_state['pages_data_infos'])

try:
    st.write(f"Number of chapters extracted: {len(st.session_state['chapters_extracted'])}")
    st.write(f"chapters extracted: {st.session_state['chapters_extracted'][0]['content'][:1000]}")
except:
    st.write("No chapters extractedyet.")

chapters_chunking(st.session_state['chapters_extracted'])

try:
    st.write(f"Number of chapters chunked: {len(st.session_state['chapters_chunked'])}")
except:
    st.write("No chapters chuncked yet.")

if st.session_state.get('chapters_dict') is not None:
    chapters = st.session_state['chapters_dict']

    if len(chapters) > 0 and isinstance(chapters[0], dict) and 'chapter_title' in chapters[0]:
        chapter_titles = ["Chapter " + str(idx) + ": " + ch['chapter_title'] for idx, ch in enumerate(chapters, start=1)]

    options = st.multiselect(
        "Select a Chapter:",
        [chapter_titles][0],
        max_selections=1,
        accept_new_options=False,
    )

    st.write(f"Selected chapter: {options[0] if options else 'None'}")











