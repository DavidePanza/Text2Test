import streamlit as st
import os
import sqlite3
import base64

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


def get_base64_encoded_image(image_path):
    """
    Reads an image file and encodes it to Base64.
    """
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def load_background_image():
    """
    Loads and displays a background image with an overlaid title.
    """
    image_path = "../images/image1.jpg"  
    base64_image = get_base64_encoded_image(image_path)
    
    # Inject CSS for the background and title overlay
    st.markdown(
        f"""
        <style>
        /* Background container with image */
        .bg-container {{
            position: relative;
            background-image: url("data:image/png;base64,{base64_image}");
            background-size: container;
            background-position: center;
            height: 250px;  /* Adjust the height of the background */
            width: 70%;
            margin: 0 auto;
            filter: contrast(110%) brightness(200%); /* Dim the brightness of the image */
            border-radius: 200px;  /* Makes the container's corners rounded */
            overflow: hidden;  
        }}

        /* Overlay for dimming effect */
        .bg-container::after {{
            content: '';
            position: absolute;
            top: ;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(20, 20, 20, 0.5); /* Semi-transparent black overlay */
            z-index: 1; /* Ensure the overlay is above the image */
        }}

        /* Overlay title styling */
        .overlay-title {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;   /* Title color */
            font-size: 70px;
            font-weight: bold;
            text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7); /* Shadow for better visibility */
            text-align: center;
            z-index: 2; /* Ensure the title is above the overlay */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create the background container with an overlaid title
    st.markdown(
        """
        <div class="bg-container">
            <div class="overlay-title">Streamlit RAG</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def upload_pdf():
    st.write("Please upload a textbook in PDF format:")
    
    if 'uploaded_file' not in st.session_state:
        st.session_state['uploaded_pdf'] = None
    
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    
    if uploaded_file is not None:
        st.session_state['uploaded_pdf'] = uploaded_file
        st.success("File uploaded successfully!")
    else:
        st.info("No file uploaded yet.")


def load_uploaded_files(uploaded_files_log):
    """
    Load the list of uploaded files from a text file.
    """
    if os.path.exists(uploaded_files_log):
        with open(uploaded_files_log, "r") as f:
            return f.read().splitlines()
    return []


def save_uploaded_files(file_list, uploaded_files_log):
    """
    Save the list of uploaded files to a text file.
    """
    with open(uploaded_files_log, "w") as f:
        f.write("\n".join(file_list))