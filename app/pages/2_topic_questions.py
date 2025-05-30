import streamlit as st
from app.utils import *
from app.main_IO import *
from app.pages.utils_chapter.display_pages import *
from app.pages.utils_chapter.display_questions import *
from app.pages.utils_chapter.chapter_extraction import *
from app.pages.utils_chapter.chapter_selection import *
from app.pages.utils_chapter.download_questions import create_docx_from_data


# Initialise
apply_style()
show_pdf_preview()
st.title("Generate Questions on a Topic")
st.write("Here, you can generate questions based on a specific topic.")

# Set up logger
level = st.selectbox("Logging level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
logging.getLogger().setLevel(getattr(logging, level))

if st.session_state['uploaded_pdf_bytes'] is not None:
    st.write("You have uploaded a PDF file. You can now generate questions based on the content of the PDF.")


# use https://docs.streamlit.io/develop/api-reference/chat/st.chat_input
# or https://docs.streamlit.io/develop/api-reference/widgets/st.text_input