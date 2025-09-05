# Text2Test 

Text2test is a web app that generates downloadable questions and answers from PDF textbooks uploaded by users, helping students prepare for exams
You can upload any PDF book or document, and let AI create questions to improve your learning experience.

You can try the app for free at this link: [Text2Test](https://huggingface.co/spaces/davidepanza/test2text)

## Features

### Two Question Generation Modes
- **Chapter-Based Questions**: Extract table of contents, select specific chapters, and generate targeted questions from chosen sections
- **Topic-Based Questions**: Input keywords or topics to generate questions from relevant content across the entire document

### AI-powered PDF Processing
- Automatic text extraction with PyMuPDF
- Intelligent page numbering correction
- Table of contents detection and parsing
- Chapter boundary identification
- PDF preview and inspection tools

### AI Integration
- **LLM**: Gemma2-12B-IT-4QAT model hosted on RunPod via Ollama
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2) for semantic search
- **Vector Database**: ChromaDB for efficient content retrieval
- Smart chunking with configurable overlap for context preservation

### Export & Download
- Generate downloadable Word documents (.docx) with all questions and answers organised by chapter or topic

## Technology Stack

### Frontend & UI
- **Streamlit**

### Backend Processing
- **PyMuPDF (fitz)**: PDF text extraction and page analysis
- **ChromaDB**: Vector database for semantic search and retrieval
- **SentenceTransformers**: Text embeddings for content similarity
- **Python-docx**: Word document generation

### AI & ML Infrastructure
- **Gemma2-12B-IT**: Large language model for question generation
- **Ollama**: Model serving framework
- **RunPod**: GPU cloud infrastructure
- **Docker**: Containerized deployment

### Text Processing Pipeline
- Intelligent text chunking with sentence-level overlap
- Table of contents extraction and cleaning
- Chapter boundary detection
- Content preprocessing and optimization

## Project Structure

```
text2test/
├── app/                          # Main application
│   ├── main.py                   # Entry point and navigation
│   ├── pages/                    # Multi-page interface
│   │   ├── 1_chapter_questions.py
│   │   ├── 2_topic_questions.py
│   │   └── 3_inspect_pdf.py
│   ├── backend/                  # Core processing modules
│   │   ├── raw_text_processing.py    # PDF extraction
│   │   ├── chromadb_utils.py         # Vector database
│   │   ├── text_processing.py        # Content chunking
│   │   ├── runpod_client.py          # AI model interface
│   │   └── messages_templates.py     # LLM prompts
│   ├── chromadb_model/          # Local embedding model
│   └── utils/                   # Helper functions
```

## How It Works

1. **Upload PDF**: Users upload their study material in PDF format
2. **Text Extraction**: PyMuPDF extracts and processes text, identifying chapters and structure
3. **Content Indexing**: Text is chunked and embedded using SentenceTransformers, stored in ChromaDB
4. **Question Generation**: 
   - **Chapter Mode**: Extract TOC, let users select chapters, generate questions from specific content
   - **Topic Mode**: Use semantic search to find relevant passages, generate focused questions
5. **AI Processing**: Gemma2-12B-IT generates contextual questions and detailed answers
6. **Export**: Download formatted questions as Word documents




