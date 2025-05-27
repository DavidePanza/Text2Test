import streamlit as st
from app.utils import *


st.title("Generate Questions from a Chapter")
st.write("Here, you can generate questions based on a specific chapter.")

if st.button("Back to Main"):
    st.switch_page("main.py")

show_pdf_preview()