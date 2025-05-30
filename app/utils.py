import streamlit as st
import logging


def configure_page() -> None:
    """
    Configures the Streamlit page.
    """
    st.set_page_config(page_title="Text2Test", 
                       layout="wide", 
                       page_icon=":book:")


def apply_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;700&display=swap');

    html, body, .stApp,
    .css-1v3fvcr, .css-ffhzg2, .css-1d391kg,
    div[data-testid="stMarkdownContainer"],
    div[data-testid="stText"],
    div[data-testid="stTextInput"],
    div[data-testid="stSelectbox"],
    div[data-testid="stCheckbox"],
    div[data-testid="stSlider"],
    label, input, textarea, button, select,
    .stButton, .stTextInput > div, .stMarkdown, .stCaption,
    .streamlit-expanderHeader, .st-expander > div,
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Work Sans', sans-serif !important;
    }

    /* Ensure bold text uses the correct font weight */
    strong, b, .stMarkdown strong, .stMarkdown b {
        font-family: 'Work Sans', sans-serif !important;
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def breaks(n=1):
    """
    Creates a line break.
    """
    if n == 1:
        st.markdown("<br>",unsafe_allow_html=True)
    elif n == 2:
        st.markdown("<br><br>",unsafe_allow_html=True)
    elif n == 3:
        st.markdown("<br><br><br>",unsafe_allow_html=True)
    else:
        st.markdown("<br><br><br><br>",unsafe_allow_html=True)


def debug_log(message):
    """Log debug messages and optionally show them in the app."""
    logging.debug(message)
    if logging.getLogger().level <= logging.DEBUG:
        st.code(f"[DEBUG] {message}", language="text")

