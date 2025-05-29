import streamlit as st
import json
from app.utils import *
from app.main_IO import *
from app.pages.ui_utils.page1_utils import *
from app.backend.raw_text_processing import *
from app.backend.get_requests import extract_chapters_from_toc, generate_questions_from_chapter, generate_questions_from_chapter_edgecase
from app.backend.text_processing import chapters_chunking
from app.backend.chunks_processing import get_chapter_context



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

    options = st.multiselect(  # use selectobx columns here https://docs.streamlit.io/develop/api-reference/data/st.column_config/st.column_config.selectboxcolumn
        "Select a Chapter:",
        [chapter_titles][0],
        max_selections=1,
        accept_new_options=False,
    )

    st.selected_chapter_title = options[0]
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


# if st.session_state['chapter_selected_chunks'] is not None:
#     if len(st.session_state['chapter_selected_chunks']) >= st.session_state['num_questions']:
#         st.session_state['chapter_prompt'] = chapter_prompt(st.session_state['chapter_selected_chunks'], st.session_state['num_questions'])
#     else:
#         st.session_state['chapter_prompt'] = chapter_prompt_edgecase(st.session_state['chapter_selected_chunks'], st.session_state['num_questions'])


if st.session_state['chapter_selected_chunks'] is not None and st.button("Generate Questions"):
    # Replace this with your actual question generation function
    with st.spinner("Generating questions..."):
        if len(st.session_state['chapter_selected_chunks']) >= st.session_state['num_questions']:
            st.session_state['raw_output'] = generate_questions_from_chapter(st.session_state['chapter_selected_chunks'], st.session_state['num_questions'])
        else:
            st.write("use edgecase prompt")
            st.session_state['questions_json'] = generate_questions_from_chapter_edgecase(st.session_state['chapter_selected_chunks'], st.session_state['num_questions'])

debug_log(f"Generated Questions: {st.session_state['questions_json']}")

breaks(2)
st.header("Generated Questions")
breaks(1)

for idx, question_item in enumerate(st.session_state['questions_json']):
    question_text = question_item['question']
    answer_text = question_item['answer']

    col1, col2 = st.columns([0.9, 0.1])
    
    with col1:
        st.html(f"<p style='font-size:20px; margin:0;'>{idx+1}. {question_text}</p>")
        col1_ = st.columns([1, 4])[0]
        with col1_:
            with st.expander("💡 Show Answer"):
                st.write(answer_text)

    with col2:
        selected = st.checkbox("📌", key=f"select_{idx}")

breaks(2)
if st.button("Append Selected Questions to Download"):
        if st.selected_chapter_title not in st.session_state.get('questions_to_download', {}):
        for idx, question in enumerate(st.session_state.get('questions_json', [])):
            if st.session_state.get(f"select_{idx}")
                st.session_state['questions_to_download'][st.selected_chapter_title] = 





                st.session_state['questions_to_download'][st.selected_chapter_title].append(question)
        selected_questions[st.selected_chapter_title] = {
        selected_questions['Questions'] = []
        for idx, question in enumerate(st.session_state.get('questions_json', [])):
            if st.session_state.get(f"select_{idx}"):
                selected_questions.append(question)
        st.session_state.questions_to_download = selected_questions
        st.success(f"{len(selected_questions)} questions saved for download!")


from docx import Document
from io import BytesIO
import streamlit as st

def create_docx_from_data(data):
    doc = Document()
    doc.add_heading("Generated Questions", 0)

    for chapter, qas in data.items():
        doc.add_heading(chapter, level=1)
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

    docx_file = create_docx_from_data(questions_data)

    st.download_button(
        label="📄 Download as Word (.docx)",
        data=docx_file,
        file_name="questions.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)
# Show what's selected (for testing)
if st.session_state.questions_to_download:
    st.markdown("### ✅ Selected Questions")
    for q in st.session_state.questions_to_download:
        st.write(q['question'])


# check https://docs.streamlit.io/develop/api-reference/execution-flow/st.form


