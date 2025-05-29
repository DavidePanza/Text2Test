import streamlit as st
from app.utils import debug_log
from app.pages.utils_chapter.chapter_extraction import *
from app.backend.raw_text_processing import *
from app.backend.get_requests import generate_questions_from_chapter, generate_questions_from_chapter_edgecase
from app.backend.text_processing import chapters_chunking
from app.backend.chunks_processing import get_chapter_context

def get_chapter_titles(chapters):
    """Generate list of chapter titles from chapters dict."""
    if chapters and isinstance(chapters[0], dict) and 'chapter_title' in chapters[0]:
        return [f"Chapter {idx}: {ch['chapter_title']}" for idx, ch in enumerate(chapters, start=1)]
    return []

def select_chapter(chapter_titles):
    """Show a multiselect for chapters, max 1 selection."""
    return st.multiselect(
        "Select a Chapter:",
        chapter_titles,
        max_selections=1,
        help="Choose one chapter to generate questions from."
    )

def select_num_questions():
    """Number input for question count."""
    return st.number_input(
        "Number of questions to generate (max 5)",
        min_value=1,
        max_value=5,
        step=1,
        format="%d",
        help="Choose how many questions to generate."
    )

def chapter_question_form():
    with st.form("chapter_question_form"):
        st.html("""
        <style>
            .range-header {
                margin-bottom: 0.5rem;
            }
        </style>
        """)
        st.html('<h3 class="range-header">Select Chapter</h3>')
        chapters = st.session_state.get('chapters_dict', [])
        chapter_titles = get_chapter_titles(chapters)

        options = select_chapter(chapter_titles)
        num_questions = select_num_questions()

        submitted = st.form_submit_button("Generate Questions")

        if submitted:
            if not options:
                st.warning("Please select a chapter before submitting.")
                return

            selected_chapter = options[0]
            selected_index = chapter_titles.index(selected_chapter)

            # Save selections in session state
            st.session_state.selected_chapter_title = selected_chapter
            st.session_state.selected_chapter_idx = selected_index
            st.session_state.num_questions = num_questions

            debug_log(f"Selected chapter: {selected_chapter}")
            debug_log(f"Selected index: {selected_index}")
            debug_log(f"Generating {num_questions} questions...")

            # Get chapter context (assumed to populate st.session_state['chapter_selected_chunks'])
            get_chapter_context(
                st.session_state['chapters_chunked'],
                selected_index,
                num_questions
            )

            debug_log(f"Selected chapter chunks: {len(st.session_state.get('chapter_selected_chunks', []))}")

            # Now trigger question generation with spinner
            chunks = st.session_state.get('chapter_selected_chunks', [])
            with st.spinner("Generating questions..."):
                if len(chunks) >= num_questions:
                    st.session_state['raw_output'] = generate_questions_from_chapter(chunks, num_questions)
                else:
                    debug_log("Using edgecase prompt because chunks < requested questions")
                    st.session_state['questions_json'] = generate_questions_from_chapter_edgecase(chunks, num_questions)