import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io


DEFAULT_SESSION_STATE = {
    'doc': None,
    'page_choice': None,
    'uploaded_pdf_name': None,
    'pdf_changed': False,
    'uploaded_pdf_bytes': None,
    'toc_page_range': None,
    'page_range_set' : False,
    'page_range_updated' : False,
    'toc': None,
    'full_text': None,
    'pages_data_infos': None,
    'chapters_starting_page': None,
    'chapters_dict': None,
    'chapters_extracted': None,
    'chapters_chunked': None,
    'selected_chapter_idx': None,
    'selected_chapter_title': None,
    'num_questions': None,
    'chapter_selected_chunks': None,
    'chapter_prompt': None,
    'questions_json': None,
    'raw_output': None,  # remove this (only for debug)
    'questions_ready': False,
    'questions_to_download' : {}
}


def initialise_session_state():
    """
    Initializes the session state variables if not already set.
    """
    for key, default_val in DEFAULT_SESSION_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = default_val


def reset_session_state_on_upload():
    """
    Resets session state variables to their default values.
    """
    for key, default_val in DEFAULT_SESSION_STATE.items():
        st.session_state[key] = default_val


def upload_pdf():
    st.write("Please upload a textbook in PDF format:")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    
    if uploaded_file is not None:
        prev_file = st.session_state.get('uploaded_pdf_name')
        if uploaded_file.name != prev_file:
            # New file detected
            reset_session_state_on_upload()
            st.session_state['pdf_changed'] = True
        else:
            st.session_state['pdf_changed'] = False

        pdf_bytes = uploaded_file.read()

        if pdf_bytes:
            st.session_state['uploaded_pdf_bytes'] = pdf_bytes
            st.session_state['uploaded_pdf_name'] = uploaded_file.name
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        else:
            st.error("Uploaded file is empty!")
                
    elif uploaded_file is None and st.session_state.get('uploaded_pdf_bytes') is not None:
        st.success("File uploaded successfully!")
    else:
        st.info("Please upload a PDF file to proceed.")


def show_pdf_preview():
    if 'uploaded_pdf_bytes' in st.session_state:
        pdf_bytes = st.session_state['uploaded_pdf_bytes']
        doc = None
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            if doc.page_count < 1:
                st.sidebar.error("PDF has no pages!")
                return
            page = doc.load_page(0)
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            st.sidebar.image(img, caption="First page preview", use_container_width=True)
        except Exception as e:
            st.sidebar.error(f"Failed to open PDF: {e}")
        finally:
            if doc is not None:
                doc.close()
    else:
        st.sidebar.write("Upload a PDF to see a preview here.")

