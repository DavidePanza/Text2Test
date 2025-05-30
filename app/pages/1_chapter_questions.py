import streamlit as st
from app.utils import *
from app.main_IO import *
from app.pages.utils_chapter.display_pages import *
from app.pages.utils_chapter.display_questions import *
from app.pages.utils_chapter.chapter_extraction import *
from app.pages.utils_chapter.chapter_selection import *
from app.download_questions import create_docx_from_data

# Set up logger
if st.session_state.use_logger: 
    level = st.selectbox("Logging level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    logging.getLogger().setLevel(getattr(logging, level))
else:
    logging.getLogger().setLevel(logging.CRITICAL + 1)

# Initialise
apply_style()

# add_sidebar_header()
st.sidebar.html("""
<div style='position: fixed; top: 10px; left: 20px; z-index: 999; padding: 10px;'>
    <h3>Menu</h3>
</div>
""")

show_pdf_preview()
st.title("Generate Questions from a Chapter")
st.divider()
st.write("""
        Here you can generate questions based on a specific chapter.  
        To do this, please first select the page range that includes the Table of Contents (TOC) — sometimes called the index or contents page — which lists the chapters and their page numbers.  

        This step is important because it helps the app automatically identify and locate chapters, so you can easily choose the exact chapter to generate questions from.
        """)

# Display the page range selector
breaks(1)
display_scrollable_pages()

# UI and Interaction
set_clicked, start_page, end_page = page_range_selector_ui()

if set_clicked:
    updated = handle_page_range_submission(start_page, end_page)
    st.session_state["page_range_updated"] = updated

if st.session_state.get("page_range_updated", False):
    extract_content_if_needed()
    st.session_state["page_range_updated"] = False

# Gate rest of app
if st.session_state.get("page_range_set", False):

    # Call the form in your main app code to generate questions
    result = chapter_question_form()
    if result:
        st.session_state.questions_dict_chapter = result
    debug_log(f"questions: {st.session_state.get('questions_dict_chapter', 'None')}")
    
    if st.session_state.get("questions_ready_chapter"):
        breaks(2)
        st.subheader("Generated Questions")
        st.divider()
        # Visualize generated questions and store them
        show_questions(st.session_state.get('questions_dict_chapter'))
        breaks(1)
        show_download_controls(st.session_state.get('selected_chapter_title'), st.session_state.get('questions_dict_chapter', 'None'))
        debug_show_selected_questions()

        with st.sidebar:
            st.markdown("---")  # Divider
            st.markdown("**Download Questions**")  # Spacing

            docx_file = create_docx_from_data(st.session_state['questions_to_download'])

            st.download_button(
                label="📄 Download as Word (.docx)",
                data=docx_file,
                file_name="questions.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                on_click="ignore"
        )
            
else:
    st.info("Please set a valid page range to continue.")




