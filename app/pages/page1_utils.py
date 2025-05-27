import streamlit as st
import fitz
import base64


def display_scrollable_pages():
    if st.session_state.get("uploaded_pdf_bytes") is not None:
        pdf_document = None
        try:
            pdf_document = fitz.open(stream=st.session_state.get("uploaded_pdf_bytes"), filetype="pdf")

            st.write("To generate questions from a chapter, please select the page range in which the Table Of Content is included.")
            st.write("This is important to automatically identify the chapter you want to generate questions from.")

            # CSS styles
            css = """ 
            <style>
            .scrolling-wrapper {
                display: flex;
                overflow-x: auto;
                padding: 10px;
                gap: 15px;
                border: 1px solid #ddd;
                margin-bottom: 20px;
            }
            .page-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 5px;
                flex-shrink: 0;
            }
            .page-image {
                height: 400px;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .page-number {
                font-weight: bold;
                font-size: 16px;
                color: #333;
            }
            </style>
            """

            # Build HTML content
            html_content = css + '<div class="scrolling-wrapper">'
            
            for page_num in range(1, st.session_state.get("chapters_starting_page")):
                page = pdf_document.load_page(page_num)
                pix = page.get_pixmap()
                img_bytes = pix.tobytes("png")
                base64_img = base64.b64encode(img_bytes).decode()

                html_content += f"""
                <div class="page-container">
                    <img class="page-image" src="data:image/png;base64,{base64_img}">
                    <div class="page-number">Page {page_num + 1}</div>
                </div>
                """
            
            html_content += '</div>'

            # Render with st.html()
            st.html(html_content)

        except Exception as e:
            st.error(f"Failed to render PDF pages: {e}")

        finally:
            if pdf_document is not None:
                pdf_document.close()

    else:
        st.warning("No PDF file uploaded. Please upload a PDF file to generate questions from a chapter.")


def get_toc_page_range():
    """
    Get the page range for the Table of Contents (TOC) from session state.
    If not set, return a default range.
    """
    if st.session_state.get("uploaded_pdf_bytes") is not None:
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