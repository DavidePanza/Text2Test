import streamlit as st
from app.utils import *
from app.main_IO import *
from app.pages.page1_utils import *


st.title("Generate Questions from a Chapter")
st.write("Here, you can generate questions based on a specific chapter.")

st.write(st.session_state.get("chapters_starting_page"))

# if st.button("Back to Main"):
#     st.switch_page("main.py")

if st.session_state.get("uploaded_pdf_bytes") is None:
    st.warning("Please upload a PDF file to generate questions from a chapter.")
else:
    pass

show_pdf_preview()
display_scrollable_pages()

# Page range selectors
with st.container():
    st.markdown("### Select Page Range")
    col1, col2 = st.columns(2)

    with col1:
        start_page = st.number_input("Start page", min_value=1, max_value=30, value=1) - 1

    with col2:
        end_page = st.number_input("End page", min_value=1, max_value=30, value=5) - 1
    if start_page > end_page:
        st.error("Start page must be less than end page.")
    page_range = (start_page, end_page)
    st.session_state['toc_page_range'] = page_range

if st.session_state['toc_page_range'] is not None:
    st.write(f"Selected page range: {st.session_state['toc_page_range'][0] + 1} to {st.session_state['toc_page_range'][1] + 1}")

