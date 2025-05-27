import streamlit as st
import os
from utils import *
from raw_text_processing import *
import fitz
from PIL import Image
import io


configure_page()

# Sidebar configuration
st.sidebar.markdown("### Navigation")
st.sidebar.write("Select a page from the sidebar to proceed.")

# Welcome message
st.title("Welcome to Test2Test!")
st.write("This app helps you generate questions from text documents or specific topics.")

# Upload PDF file
upload_pdf()



# if __name__ == "__main__":

#     breaks(2)
#     st.write(
#         """
#     Welcome to this Streamlit app!
#     """
#     )
#     breaks(1)

#  as I have a lot of .py code for backend pèrocessing, should I keep my app files in a different folder?

    # if uploaded_file is not None:
    #     pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    #     total_pages = min(pdf_document.page_count, 30)  # Limit to 30 pages max

    #     st.write(f"Showing first {total_pages} pages")

    #     # CSS styles
    #     css = """
    #     <style>
    #     .scrolling-wrapper {
    #         display: flex;
    #         overflow-x: auto;
    #         padding: 10px;
    #         gap: 15px;
    #         border: 1px solid #ddd;
    #         margin-bottom: 20px;
    #     }
    #     .page-container {
    #         display: flex;
    #         flex-direction: column;
    #         align-items: center;
    #         gap: 5px;
    #         flex-shrink: 0;
    #     }
    #     .page-image {
    #         height: 400px;
    #         border: 1px solid #ccc;
    #         border-radius: 4px;
    #         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    #     }
    #     .page-number {
    #         font-weight: bold;
    #         font-size: 16px;
    #         color: #333;
    #     }
    #     </style>
    #     """

    #     # Build HTML content
    #     html_content = css + '<div class="scrolling-wrapper">'
        
    #     for page_num in range(total_pages):
    #         page = pdf_document.load_page(page_num)
    #         pix = page.get_pixmap()
    #         img_bytes = pix.tobytes("png")
    #         base64_img = base64.b64encode(img_bytes).decode()

    #         html_content += f"""
    #         <div class="page-container">
    #             <img class="page-image" src="data:image/png;base64,{base64_img}">
    #             <div class="page-number">Page {page_num + 1}</div>
    #         </div>
    #         """
        
    #     html_content += '</div>'

    #     # Render with st.html()
    #     st.html(html_content)

    # # ---- Vector Store Setup ----
    # # Initialize ChromaDB and collection
    # EMBEDDING_MODEL = "all-MiniLM-L6-v2"  
    # client, embedding_func = initialize_chromadb(EMBEDDING_MODEL)
    # collection_name = "my_collection"
    # collection = initialize_collection(client, embedding_func, collection_name)

    # # Define the directory for storing uploaded file names
    # database_dir = get_database_directory()
    # UPLOADED_FILES_LOG = os.path.join(database_dir, "uploaded_files.txt")

