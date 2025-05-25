def get_toc_extraction_messages(toc_text: str):
    return [
        {
            "role": "system",
            "content": "You are a precise document parser that extracts structured information from table of contents. You NEVER hallucinate..."
        },
        {
            "role": "user",
            "content": "I need to extract main chapter information from this table of contents. Only extract numbered chapters..."
        },
        {
            "role": "assistant",
            "content": "I understand. I will extract ONLY the main chapters that are explicitly shown..."
        },
        {
            "role": "user",
            "content": f"""Here is the table of contents:

{toc_text}

WARNING: DO NOT HALLUCINATE OR INVENT INFORMATION
... (rest of your instructions here)
"""
        }
    ]