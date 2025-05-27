from nltk.tokenize import sent_tokenize
import nltk
import streamlit as st

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

def text_chunking(text, max_words=750, min_words=400, overlap_sentences=5):
    """
    Creates text chunks up to max_words using sentences as undivisible units.
    Each chunk can overlap with the next one by overlap_sentences.
    Chunks smaller than min_words are merged with the next chunk.
    """
    sentences = sent_tokenize(text)
    word_counts = [len(sentence.split()) for sentence in sentences]
    
    chunks = []
    i = 0
    
    while i < len(sentences):
        chunk_sentences = []
        word_count = 0
        chunk_start = i
        
        # Build chunk
        while i < len(sentences):
            if word_count + word_counts[i] > max_words and chunk_sentences:
                break
            chunk_sentences.append(sentences[i])
            word_count += word_counts[i]
            i += 1
        
        if chunk_sentences:
            chunks.append(" ".join(chunk_sentences))
            
            # Add overlap for next chunk
            if i < len(sentences):
                chunk_size = len(chunk_sentences)
                overlap = min(overlap_sentences, chunk_size - 1)
                i = max(i - overlap, chunk_start + 1)
    
    # Merge small chunks with next chunk
    merged_chunks = []
    i = 0
    while i < len(chunks):
        current_chunk = chunks[i]
        current_words = len(current_chunk.split())
        
        # If current chunk is too small and there's a next chunk, merge them
        if current_words < min_words and i + 1 < len(chunks):
            next_chunk = chunks[i + 1]
            next_words = len(next_chunk.split())
            
            # Only merge if combined size won't be too large
            if current_words + next_words <= max_words:
                merged_chunk = current_chunk + " " + next_chunk
                merged_chunks.append(merged_chunk)
                i += 2  # Skip next chunk since we merged it
            else:
                # Keep small chunk as-is if merging would be too large
                merged_chunks.append(current_chunk)
                i += 1
        else:
            merged_chunks.append(current_chunk)
            i += 1
    
    # Remove chunks that are too long (likely data blocks or malformed content)
    final_chunks = []
    for chunk in merged_chunks:
        if len(chunk.split()) <= 1000:
            final_chunks.append(chunk)
    
    return final_chunks


def chapters_chunking(chapters, max_words=500, min_words=300, overlap_sentences=5):
    """
    Chunk the chapters into smaller parts based on word count and overlap.
    
    :param chapters: List of chapter dictionaries.
    :param max_words: Maximum number of words per chunk.
    :param min_words: Minimum number of words per chunk.
    :param overlap_sentences: Number of sentences to overlap between chunks.
    :return: List of dictionaries with chapter information and their respective chunks.
    """
    st.session_state['chapters_chunked'] = [
        {
            'chapter_number': chapter['chapter_number'],
            'chapter_title': chapter['chapter_title'],
            'chunks': text_chunking(chapter['content'], max_words, min_words, overlap_sentences)
        }
        for chapter in chapters
    ]