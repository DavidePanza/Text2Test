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
                height: 450px;
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


def select_chapter():
    """
    Displays a radio button selection for chapters extracted from the TOC.
    """
    if st.session_state.get('chapters_dict') is not None:
        chapters = st.session_state['chapters_dict']

        with st.container():
            # Custom CSS for chapter selection
            st.html("""
            <style>
                /* Bigger chapter header */
                .chapter-header {
                    font-size: 1.5rem !important;
                    font-weight: 1000 !important;
                    margin-bottom: 1rem !important;
                }
                
                /* Spaced out radio buttons */
                .stRadio > div {
                    gap: 1px;  /* Space between options */
                }
                
                /* Larger radio button labels */
                .stRadio [class*="st-"] label {
                    font-size: 8rem !important;
                    padding: 10px 15px !important;
                    border-radius: 30px;
                    transition: all 0.s ease;
                }
                
                /* Hover effect */
                .stRadio [class*="st-"] label:hover {
                    background-color: #f0f0f0;
                }
                
                /* Bigger radio buttons */
                .stRadio [class*="st-"] input+span {
                    transform: scale(2);
                    margin-right: 12px;
                }
                
                /* Selected item highlight */
                .stRadio [class*="st-"] input:checked+span {
                    color: #1a73e8;
                }
                    
            """)
            
            st.html('<div class="chapter-header">Select a Chapter</div>')
            
            # Extract titles safely
            if len(chapters) > 0 and isinstance(chapters[0], dict) and 'chapter_title' in chapters[0]:
                chapter_titles = [ch['chapter_title'] for ch in chapters]
            else:
                chapter_titles = chapters  # fallback to list of strings

            # Use columns for centered layout with comfortable padding
            col1, col2, col3 = st.columns([0.1, 10, 10])
            with col2:
                selected_chapter = st.radio(
                    "",
                    options=chapter_titles,
                    label_visibility="collapsed",  # We use our styled header instead
                    index=0  # Default to first option
                )