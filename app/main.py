import streamlit as st
from utils import *
from backend.raw_text_processing import *


# Configuration
configure_page()
initialise_session_state()

# Get current page or default to "main"
page = st.query_params.get("page", ["main"])[0]

def set_page(page_name):
    st.query_params = {"page": [page_name]}

if page == "chapter_questions":
    st.title("Chapter Questions Page")
    st.button("Back to Main", on_click=set_page, args=("main",))
    # Add your chapter questions content here

elif page == "topic_questions":
    st.title("Topic Questions Page")
    st.button("Back to Main", on_click=set_page, args=("main",))
    # Add your topic questions content here

else:
    # Main Page Content
    st.title("Welcome to Test2Test!")
    st.write("This app helps you generate questions from text documents or specific topics.")

    # Upload PDF file
    upload_pdf()
    breaks(2)

    # Main content buttons
    st.write("Please choose an option to generate questions:")
    cols = st.columns(2)
    st.html("""
    <style>
    div.stButton > button:first-child {
        width: 100%;
        padding: 30px 0;
        font-size: 20px;
        background-color: #cce5ff;
        border-radius: 10px;
        border: 2px solid #339af0;
    }
    div.stButton > button:first-child:hover {
        background-color: #99ccff;
    }
    </style>
    """)
    
    with cols[0]:
        st.button("Generate Questions on a Topic", 
                 on_click=set_page, 
                 args=("topic_questions",),
                 key="main_topic")
    
    with cols[1]:
        st.button("Generate Questions from a Chapter", 
                 on_click=set_page, 
                 args=("chapter_questions",),
                 key="main_chapter")
# # Page selection
# PAGES = {
#     "topic": "Topic Questions",
#     "chapter": "Chapter Questions"
# }

# # Set default page if not specified
# if "page" not in st.query_params:
#     st.query_params.page = "main"

# # Navigation handling
# if st.query_params.page == "topic":
#     st.switch_page("pages/2_topic_questions.py")
# elif st.query_params.page == "chapter":
#     st.switch_page("pages/1_chapter_questions.py")
# else:
#     # Welcome message
#     st.title("Welcome to Test2Test!")
#     st.write("This app helps you generate questions from text documents or specific topics.")

#     # Upload PDF file
#     upload_pdf()
#     breaks(2)

#     # Main content buttons
#     st.write("Please choose an option to generate questions:")
#     cols = st.columns(2)
#     st.html("""
#     <style>
#     div.stButton > button:first-child {
#         width: 100%;
#         padding: 30px 0;
#         font-size: 20px;
#         background-color: #cce5ff;
#         border-radius: 10px;
#         border: 2px solid #339af0;
#     }
#     div.stButton > button:first-child:hover {
#         background-color: #99ccff;
#     }
#     </style>
#     """)
#     with cols[0]:
#         if st.button("Generate Questions on a Topic", key="main_topic"):
#             st.query_params.page = "topic"
#             st.rerun()
#     with cols[1]:
#         if st.button("Generate Questions from a Chapter", key="main_chapter"):
#             st.query_params.page = "chapter"
#             st.rerun()


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

