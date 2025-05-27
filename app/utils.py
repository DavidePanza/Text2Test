import streamlit as st


def configure_page() -> None:
    """
    Configures the Streamlit page.
    """
    st.set_page_config(page_title="Text2Test", 
                       layout="wide", 
                       page_icon=":book:")


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


