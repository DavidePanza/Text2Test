import streamlit as st
from app.utils import debug_log
from app.backend.get_requests import extract_chapters_from_toc
from app.backend.raw_text_processing import extract_toc, extract_chapters

def page_range_selector():
    with st.container(border=True):
        # Header with better spacing
        st.html("""
        <style>
            .range-header {
                margin-bottom: 0.5rem;
            }
            .range-feedback {
                margin-top: 0.5rem;
            }
        </style>
        """)
        
        st.html('<h3 class="range-header">Select Page Range</h3>')
        
        # Columns with adjusted spacing
        col1, col2, _, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            start_page = st.number_input(
                "Start page",
                min_value=2,
                max_value=st.session_state.get("chapters_starting_page", 30),
                value=2,
                key="start_page",
                help="First page to include"
            )
        
        with col2:
            end_page = st.number_input(
                "End page",
                min_value=2,
                max_value=st.session_state.get("chapters_starting_page", 30),
                value=2,
                key="end_page",
                help="Last page to include"
            )
        
        # Button with better styling and feedback
        with col4:
            st.write("")  # Vertical alignment spacer
            if st.button("**Set Page Range**", 
                        use_container_width=True,
                        help="Apply the selected page range"):

                selected_page_range = (start_page-1, end_page-1)
                st.session_state.page_range_set = True

                # Extract TOC
                if st.session_state.page_range_set is True and selected_page_range != st.session_state.toc_page_range:
                    st.session_state['toc_page_range'] = selected_page_range
                    debug_log(f"Selected page range: {st.session_state['toc_page_range'][0] + 1} to {st.session_state['toc_page_range'][1] + 1}")
                    extract_toc(st.session_state.toc_page_range)
                    debug_log(f"Table of Contents (TOC): {st.session_state['toc'][:200]}...")

                    if st.session_state.toc is not None and st.session_state.chapters_dict is None:
                        with st.spinner("Extracting chapters from TOC..."):
                            extract_chapters_from_toc(st.session_state.toc)
                            st.success("Chapters extracted successfully.")

                        extract_chapters(st.session_state['chapters_dict'], st.session_state['pages_data_infos'])
                        try:
                            debug_log(f"Number of chapters extracted: {len(st.session_state['chapters_extracted'])}")
                            debug_log(f"First chapter content preview:\n{st.session_state['chapters_extracted'][0]['content'][:1000]}")
                        except KeyError:
                            debug_log("'chapters_extracted' not found in session state.")
                        except IndexError:
                            debug_log("'chapters_extracted' list is empty.")



