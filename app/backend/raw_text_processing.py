import fitz  # PyMuPDF
import warnings
import streamlit as st


def extract_page_data_fitz(doc):
    """
    Extracts page numbers and text from a PDF file using PyMuPDF.
    The function looks for page numbers in the top and bottom 15% of each page.
    It returns a list of dictionaries, each containing the page index, page number,
    and the full text of the page.
    """
    pages_data = []

    for i, page in enumerate(doc):
        height = page.rect.height
        width = page.rect.width

        top_rect = fitz.Rect(0, 0, width, height * 0.15)
        bottom_rect = fitz.Rect(0, height * 0.85, width, height)

        top_text = page.get_text("text", clip=top_rect).split()
        bottom_text = page.get_text("text", clip=bottom_rect).split()

        found_number = next((int(text) for text in top_text + bottom_text if text.isdigit()), None)
        full_text = page.get_text("text")

        pages_data.append({
            "index": i,
            "number": found_number,
            "content": full_text
        })

    return pages_data


def correct_page_numbers(pages_data, sequence_length=10):
    """
    Corrects page numbers by finding the first sequence of consecutive values, 
    filling gaps forward and backward, and setting values < 1 to None. 
    Returns the index of the first page numbered 1, or None if no sequence is found.
    """
    try:
        seen = [(i, d["number"]) for i, d in enumerate(pages_data) if isinstance(d["number"], int)]

        for start in range(len(seen) - sequence_length + 1):
            if all(seen[start + j][1] == seen[start][1] + j for j in range(sequence_length)):
                base_index, base_number = seen[start]
                break
        else:
            return None

        for offset, page in enumerate(pages_data[base_index:], start=0):
            page["number"] = base_number + offset

        for offset in range(1, base_index + 1):
            page = pages_data[base_index - offset]
            page["number"] = base_number - offset

        for page in pages_data:
            if page["number"] < 1:
                page["number"] = None

        return next((page['index'] for page in pages_data if page["number"] == 1), None)

    except Exception:
        return None


def extract_text(doc, start_chapter=None):
    """
    Extracts the text of the book starting from the specified page index.
    If no start_chapter is provided, it returns the whole doc.
    """
    if start_chapter is not None:
        all_pages_text = [
            doc[page_range].get_text("text")
            for page_range in range(start_chapter, len(doc))
        ]
        return "\n".join(all_pages_text) 
    else:
        warnings.warn(
            "No chapter start has been detected: extracting text from the entire PDF.",
            UserWarning
        )
        return "\n".join(page.get_text("text") for page in doc)
    

def process_pdf():
    """
    Processes a PDF file to extract text starting from the first chapter.
    """
    pdf_bytes = st.session_state.get("uploaded_pdf_bytes")
    if not pdf_bytes:
        st.error("No PDF uploaded.")
        return

    with st.spinner("Processing uploaded file..."):
        pdf_bytes = st.session_state.get("uploaded_pdf_bytes")
        if pdf_bytes is None:
            st.error("No PDF uploaded.")
            return

        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            # Extract data once
            pages_data_infos = extract_page_data_fitz(doc)
            chapters_starting_page = correct_page_numbers(pages_data_infos)
            full_text = extract_text(doc, chapters_starting_page)

        # Store results
        st.session_state['full_text'] = full_text
        st.session_state['pages_data_infos'] = pages_data_infos
        st.session_state['chapters_starting_page'] = chapters_starting_page


def extract_pages_range(page_range):
    """
    Extracts text from specific pages in a PDF file using PyMuPDF.
    This is used to extract TOC based on a given range of page numbers indicated by the user.
    """
    pdf_bytes = st.session_state.get("uploaded_pdf_bytes")
    if pdf_bytes is None:
        st.error("No PDF uploaded.")
        return ""

    chapters_content_list = []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page_num in page_range:
            if 0 <= page_num < len(doc):
                text = doc[page_num].get_text("text")
                chapters_content_list.append(text)
            else:
                print(f"Warning: Page number {page_num} is out of bounds.")

    toc_text = "\n".join(chapters_content_list)
    st.session_state["toc"] = toc_text


def extract_chapters(chapters_dict, pages_data_corrected):
    """
    Extract chapters from the provided JSON and pages data.
    Args:
        chapters_json (list): List of chapter dictionaries from the TOC.
        pages_data_corrected (list): List of page data dictionaries with content.
    Returns:
        list: List of dictionaries, each containing chapter details and content.
    """
    # Initialize an empty list to hold chapter dictionaries
    chapters = []
    
    # Iterate through each chapter in the JSON
    for chapter in chapters_dict:
        start_page = chapter['start_page']
        end_page = chapter['end_page']
        chapter_text = []

        # Extract content for the chapter from the pages data
        for chapter_range in range(start_page-1, end_page):
            chapter_text.append(pages_data_corrected[chapter_range]['content'])

        chapter_text = ' '.join(chapter_text)

        # Create a dictionary for the chapter
        chapter_dict = {
            'chapter_number': chapter['chapter_number'],
            'chapter_title': chapter['chapter_title'],
            'start_page': start_page,
            'end_page': end_page,
            'content': chapter_text
        }

        chapters.append(chapter_dict)
    
    st.session_state['chapters_extracted'] = chapters