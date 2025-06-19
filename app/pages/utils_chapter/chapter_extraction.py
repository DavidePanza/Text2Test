import streamlit as st
from app.utils import debug_log, breaks
from app.backend.get_requests import extract_chapters_from_toc
from app.backend.raw_text_processing import extract_chapters
from app.backend.text_processing import chapters_chunking
from app.backend.toc_cleaning import extract_font_info, extract_lines_from_font_info, TextCleaner


def page_range_selector_ui():
    with st.container(border=True):
        st.subheader("Page Range Selection")
        breaks(1)
        col1, col2, _, col4 = st.columns([1, 1, 1, 1])

        with col1:
            start_page = st.number_input(
                "Start page",
                min_value=2,
                max_value=st.session_state.get("chapters_starting_page", 30),
                value=2,
                key="start_page",
                help="First page to include"
            )

        with col2:
            end_page = st.number_input(
                "End page",
                min_value=2,
                max_value=st.session_state.get("chapters_starting_page", 30),
                value=2,
                key="end_page",
                help="Last page to include"
            )

        with col4:
            st.write("")  # spacer
            return st.button("**Set Page Range**", use_container_width=True), start_page, end_page


def handle_page_range_submission(start_page, end_page):
    selected_page_range = (start_page - 1, end_page - 1)
    current_range = st.session_state.get("toc_page_range")

    if current_range != selected_page_range:
        st.session_state["toc_page_range"] = selected_page_range
        st.session_state["page_range_set"] = True

        # Clear previous TOC and chapter data
        st.session_state["toc"] = None
        st.session_state["chapters_dict"] = None
        st.session_state["chapters_extracted"] = None

        return True  # signal update happened
    return False


def extract_content_if_needed():
    """Extract TOC and chapters if not already done."""
    toc_page_tuple = st.session_state.get("toc_page_range")
    toc_page_range = range(toc_page_tuple[0], toc_page_tuple[1] + 1)
    pdf_bytes = st.session_state.get("uploaded_pdf_bytes")
    debug_log(f"page range: {toc_page_range}")

    # Extract raw toc and clean it
    font_info = extract_font_info(pdf_bytes, toc_page_range)
    lines = extract_lines_from_font_info(font_info)
    cleaner = TextCleaner()
    st.session_state['toc'] = cleaner.process(lines)
    debug_log(f"TOC preview: {st.session_state.get('toc', '')[:200]}...")

    # Extract chapters dictionary if not already present
    if st.session_state.get("toc") and st.session_state.get("chapters_dict") is None:
        with st.spinner("Extracting chapters from TOC..."):
            extract_chapters_from_toc(st.session_state["toc"])
            st.success("Chapters extracted successfully.")

    # Extract chapters content
    chapters_dict = st.session_state.get("chapters_dict")
    debug_log(f"Chapters preview: {chapters_dict}")
    pages_data_infos = st.session_state.get("pages_data_infos")

    if chapters_dict and pages_data_infos:
        extract_chapters(chapters_dict, pages_data_infos)

        chapters_extracted = st.session_state.get("chapters_extracted")
        if chapters_extracted:
            debug_log(f"Chapters extracted: {len(chapters_extracted)}")
            debug_log(f"Preview:\n{chapters_extracted[0].get('content', '')[:1000]}")
        else:
            debug_log("Chapters not found or empty.")
    else:
        debug_log("Missing 'chapters_dict' or 'pages_data_infos'; skipping chapter extraction.")

    # Chunk chapters if extracted
    chapters_extracted = st.session_state.get("chapters_extracted")
    if chapters_extracted:
        try:
            chapters_chunking(chapters_extracted)
            debug_log(f"Number of chapters chunked: {len(st.session_state.get('chapters_chunked', []))}")
        except Exception as e:
            debug_log(f"Chapter chunking failed: {e}")
    else:
        debug_log("Skipping chapter chunking due to missing or empty 'chapters_extracted'.")