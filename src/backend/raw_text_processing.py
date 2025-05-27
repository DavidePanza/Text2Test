import fitz  # PyMuPDF
import warnings


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
    

def process_pdf(pdf_path):
    """
    Processes a PDF file to extract text starting from the first chapter.
    """
    doc = fitz.open(pdf_path)

    pages_data = extract_page_data_fitz(doc)
    start_chapter = correct_page_numbers(pages_data)
    full_text = extract_text(doc, start_chapter)

    doc.close()
    return full_text, pages_data, start_chapter


def extract_pages_range(pdf_path, page_range):
    """
    Extracts text from specific pages in a PDF file using PyMuPDF.
    This is used to extract toc based on a given range of page numbers indicated by the user.
    """
    chapters_content_list = []
    with fitz.open(pdf_path) as doc:
        for page_num in page_range:
            if 0 <= page_num < len(doc):
                text = doc[page_num].get_text("text")
                chapters_content_list.append(text)
            else:
                print(f"Warning: Page number {page_num} is out of bounds.")
    return "\n".join(chapters_content_list)


def extract_chapters(chapters_json, pages_data_corrected):
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
    for chapter in chapters_json:
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
    
    return chapters