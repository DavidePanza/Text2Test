import streamlit as st
from docx import Document
from io import BytesIO
from datetime import datetime
from app.utils import *
from app.main_IO import *
from app.pages.utils_chapter.page1_utils import *
from app.pages.utils_chapter.display_questions import *
from app.pages.utils_chapter.chapter_extraction import *
from app.pages.utils_chapter.chapter_selection import *
from app.backend.raw_text_processing import *


st.title("Generate Questions from a Chapter")
st.write("Here, you can generate questions based on a specific chapter.")

# if st.session_state.get("uploaded_pdf_bytes") is None:
#     st.warning("Please upload a PDF file to generate questions from a chapter.")
# else:
#     pass

level = st.selectbox("Logging level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
logging.getLogger().setLevel(getattr(logging, level))

# Display the PDF preview and page range selector
show_pdf_preview()
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
    chapter_question_form()
    debug_log(f"questions: {st.session_state.get('questions_json', 'None')}")
    breaks(2) 
                
    if st.session_state.get("questions_ready"):
        # Visualize generated questions and store them
        show_questions()
        show_download_controls()
        debug_show_selected_questions()
   
else:
    st.info("Please set a valid page range to continue.")





# # breaks(2)

# # debug_log(f"Questions JSON: {st.session_state.get('questions_json', [])}")

# col1_download, col2_download, col3_download = st.columns([0.3, 0.3, 0.6])
# with col1_download:
#     if st.button("Sync Selected Questions to Download"):
#         selected_chapter = st.session_state.get('selected_chapter_title')
#         if selected_chapter is None:
#             st.error("No chapter selected!")
#         else:
#             if selected_chapter not in st.session_state['questions_to_download']:
#                 st.session_state['questions_to_download'][selected_chapter] = []

#             current_selected = st.session_state['questions_to_download'][selected_chapter]

#             for idx, question in enumerate(st.session_state.get('questions_json', [])):
#                 current_question = {'question': question['question'], 'answer': question['answer']}
#                 checkbox_key = f"select_{idx}"
#                 is_selected = st.session_state.get(checkbox_key, False)

#                 if is_selected and current_question not in current_selected:
#                     current_selected.append(current_question)
#                 elif not is_selected and current_question in current_selected:
#                     current_selected.remove(current_question)

#             st.success(f"Selected questions synced for chapter '{selected_chapter}'.")

# with col2_download:
#     if st.button("Clear Selected Questions"):
#         st.session_state['questions_to_download'] = {}
#         st.success("Cleared all selected questions.")


# # Show what's selected (for testing)
# if st.session_state.questions_to_download:
#     st.markdown("### ✅ Selected Questions")
#     for chapter, questions_list in st.session_state.questions_to_download.items():
#         st.markdown(f"#### {chapter}")
#         for q in questions_list:
#             st.write(q['question'])



def create_docx_from_data(data):
    doc = Document()
    doc.add_heading("Questions", 0)
    doc.add_paragraph(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    for chapter, qas in data.items():
        doc.add_heading(chapter, level=1)
        doc.add_paragraph("")  # Spacing
        for idx, qa in enumerate(qas, 1):
            doc.add_paragraph(f"Q{idx}: {qa['question']}", style='List Number')
            doc.add_paragraph(f"A: {qa['answer']}", style='Normal')
            doc.add_paragraph("")  # Spacing

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


with st.sidebar:
    st.markdown("---")  # Divider
    st.write("")  # Spacing

    docx_file = create_docx_from_data(st.session_state.get('questions_to_download', {}))

    st.download_button(
        label="📄 Download as Word (.docx)",
        data=docx_file,
        file_name="questions.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)


# check https://docs.streamlit.io/develop/api-reference/execution-flow/st.form


