import streamlit as st
from app.utils import *


st.title("Generate Questions on a Topic")
st.write("Here, you can generate questions based on a specific topic.")

if st.button("Back to Main"):
    st.switch_page("main.py")

show_pdf_preview()

if st.session_state['uploaded_pdf'] is not None:
    st.write("You have uploaded a PDF file. You can now generate questions based on the content of the PDF.")