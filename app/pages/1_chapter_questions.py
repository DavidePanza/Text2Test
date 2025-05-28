import streamlit as st
import json
from app.utils import *
from app.main_IO import *
from app.pages.ui_utils.page1_utils import *
from app.backend.raw_text_processing import *
from app.backend.toc_parser import extract_chapters_from_toc
from app.backend.text_processing import chapters_chunking
from app.backend.chunks_processing import get_chapter_context
from app.backend.messages_templates import chapter_prompt, chapter_prompt_edgecase
from app.backend.runpod_client import run_prompt


st.title("Generate Questions from a Chapter")
st.write("Here, you can generate questions based on a specific chapter.")

# if st.session_state.get("uploaded_pdf_bytes") is None:
#     st.warning("Please upload a PDF file to generate questions from a chapter.")
# else:
#     pass

show_pdf_preview()
display_scrollable_pages()
page_range_selector()

if st.session_state['toc_page_range'] is not None:
    debug_log(f"Selected page range: {st.session_state['toc_page_range'][0] + 1} to {st.session_state['toc_page_range'][1] + 1}")

    extract_toc(st.session_state['toc_page_range'])
    debug_log(f"Table of Contents (TOC): {st.session_state['toc'][:200]}...")

if st.session_state['toc'] is not None and st.session_state['chapters_dict'] is None:
    with st.spinner("Extracting chapters from TOC..."):
        extract_chapters_from_toc(st.session_state['toc'])
        st.success("Chapters extracted successfully.")

try:
    debug_log(f"Chapters dictionary: {st.session_state['chapters_dict'][0]}")
    debug_log(f"Pages data infos: {st.session_state['pages_data_infos'][0]}")
except:
    pass

extract_chapters(st.session_state['chapters_dict'], st.session_state['pages_data_infos'])

try:
    debug_log(f"Number of chapters extracted: {len(st.session_state['chapters_extracted'])}")
    debug_log(f"First chapter content preview:\n{st.session_state['chapters_extracted'][0]['content'][:1000]}")
except KeyError:
    debug_log("'chapters_extracted' not found in session state.")
except IndexError:
    debug_log("'chapters_extracted' list is empty.")


chapters_chunking(st.session_state['chapters_extracted'])

try:
    debug_log(f"Number of chapters chunked: {len(st.session_state['chapters_chunked'])}")
except:
    debug_log("'chapters_chunked' not found in session state.")

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

# Get the index of the selected title
if options:
    st.session_state['selected_chapter_idx'] = chapter_titles.index(options[0])
    st.write(f"Selected index: {st.session_state['selected_chapter_idx']}")


num_questions = st.number_input(
    "Number of questions to generate (max 10)",
    min_value=1,
    max_value=5,
    value=None,
    step=1
)

# Optionally store it in session_state
st.session_state['num_questions'] = num_questions

if st.session_state['num_questions'] is not None:
    get_chapter_context(st.session_state['chapters_chunked'],
                        st.session_state['selected_chapter_idx'],
                        num_questions)

    debug_log(f"Selected chapter chunks: {len(st.session_state['chapter_selected_chunks'])}")


if st.session_state['chapter_selected_chunks'] is not None:
    if len(st.session_state['chapter_selected_chunks']) >= st.session_state['num_questions']:
        st.session_state['chapter_prompt'] = chapter_prompt(st.session_state['chapter_selected_chunks'], st.session_state['num_questions'])
    else:
        st.session_state['chapter_prompt'] = chapter_prompt_edgecase(st.session_state['chapter_selected_chunks'], st.session_state['num_questions'])


if st.button("Generate Questions"):
    # Replace this with your actual question generation function
    with st.spinner("Generating questions..."):
        questions = run_prompt(st.session_state['chapter_prompt'])
        st.write(f"Generated Questions: {questions}")



