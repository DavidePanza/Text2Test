import fitz  
import re
import streamlit as st
from app.utils import debug_log, breaks


def extract_font_info(pdf_bytes, content_page_ranges, header_margin=70, footer_margin=100):
    try:
        # If pdf_bytes is a BytesIO object
        if hasattr(pdf_bytes, 'read'):
            pdf_bytes.seek(0)  # Reset pointer
            pdf_bytes = pdf_bytes.read()
        
        # Ensure it's bytes, not string
        if isinstance(pdf_bytes, str):
            pdf_bytes = pdf_bytes.encode()
            
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        debug_log(f"PDF opened successfully. Pages: {len(doc)}")
        
    except Exception as e:
        st.error(f"Error opening PDF: {e}")
        return []
    
    font_data = []
    
    for page_num in content_page_ranges:
        page = doc.load_page(page_num)
        page_height = page.rect.height
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        y = span["origin"][1]
                        # Skip headers/footers using defaults
                        if y < header_margin or y > (page_height - footer_margin):
                            continue
                        font_data.append({
                            "text": span["text"],
                            # "font_name": span["font"],
                            # "font_size": span["size"],
                            # "color": span["color"],  # RGB tuple (e.g., (0, 0, 0) for black)
                            # "is_bold": "bold" in span["font"].lower(),
                            # "is_italic": "italic" in span["font"].lower(),
                            "page": page_num + 1,
                            "coordinates": (span["origin"][0], span["origin"][1])
                        })
    return font_data


def extract_lines_from_font_info(font_info):
    """
    Extracts lines of text from font information based on y-coordinates.
    This function assumes that text elements with the same y-coordinate belong to the same line.
    """
    if not font_info:
        return []
    lines = []
    prev_y = None
    cur_line = ""

    for element in font_info:
        cur_y = element['coordinates'][1]
        if prev_y is None or cur_y == prev_y:
            cur_line += " " + element['text']
        else:
            if cur_line.strip():
                lines.append(cur_line.strip())
            cur_line = element['text']
        prev_y = cur_y

    # Don't forget the last line
    if cur_line.strip():
        lines.append(cur_line.strip())

    return lines


class TextCleaner:
    def __init__(self):
        self.patterns = {
            # patterns to filter out unwanted lines
            'numbered_lines': re.compile(r'^\d+\.\d+\b'),
            'symbol_only': re.compile(r'^[\W_]+$'),
            'copyright_pattern': re.compile(r'(©|ⓒ|\(c\)|\(C\)|c\s*⃝)', re.IGNORECASE),
            'exercises_pattern': re.compile(r'^\s*Exercises?\b[\s\d.:!?-]*$', re.IGNORECASE),
            # noise patterns
            'dotted_noise': re.compile(r'(?<!\w)([.\s]){3,}(?!\w)'),  
            'symbol_noise': re.compile(r'(?<!\w)([\W]\s?){3,}(?!\w)')
            }

    def filter_lines(self, lines):
        """Remove unwanted lines while keeping the structure"""
        return [
            line for line in lines
            if not (self.patterns['numbered_lines'].match(line.strip()) or 
                   self.patterns['symbol_only'].match(line.strip()) or
                   self.patterns['copyright_pattern'].search(line.strip()) or
                   self.patterns['exercises_pattern'].match(line.strip())) 
        ]

    def filter_noise(self, lines):
        """Remove noise patterns from lines"""
        cleaned = []
        for line in lines:
            # Remove standalone noise sequences (not between words)
            line = self.patterns['dotted_noise'].sub('', line)
            line = self.patterns['symbol_noise'].sub('', line)
            cleaned.append(line.strip())
        return cleaned
    
    def process(self, lines):
        """Complete processing pipeline"""
        filtered = self.filter_lines(lines)
        cleaned = self.filter_noise(filtered)
        return cleaned