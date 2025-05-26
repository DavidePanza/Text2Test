def get_toc_extraction_messages(toc_text: str):
    return [
        {
            "role": "system",
            "content": "You are a precise document parser that extracts structured information from table of contents. You NEVER hallucinate You NEVER hallucinate, invent, or make up information. You ONLY extract what is explicitly present in the provided text. If you cannot find clear chapter information, you return an empty array. You do not guess chapter titles or page numbers."
        },
        {
            "role": "user",
            "content": "I need to extract main chapter information from this table of contents. Only extract numbered chapters, ignore subsections. Do not make up any information."
        },
        {
            "role": "assistant",
            "content": "I understand. I will extract ONLY the main chapters that are explicitly shown in your table of contents. I will not invent, guess, or hallucinate any chapter titles or page numbers. I will only use the exact information present in the document."
        },
        {
            "role": "user",
            "content": f"""Here is the table of contents:

        {toc_text}

        WARNING: DO NOT HALLUCINATE OR INVENT INFORMATION
        - Do NOT make up chapter titles like "Probability", "Statistical Inference", "Linear Regression"
        - Do NOT guess page numbers
        - Do NOT create generic textbook chapters
        - ONLY extract what you can clearly see in the provided text

        CRITICAL RULES:
        1. Extract ONLY main chapters that start with a number (1, 2, 3, etc.)
        2. Do NOT extract subsections (like 1.1, 1.2, 2.1, etc.)
        3. Use the EXACT chapter titles shown in the document
        4. Use the EXACT page numbers shown in the document
        5. Handle both roman numerals (i, ii, iii, v, x) and arabic numerals (1, 25, 100)
        6. Calculate end pages as: next chapter's start page minus 1
        7. Return ONLY valid JSON - no explanations, no markdown formatting
        8. If you cannot clearly identify chapters, return empty array []

        Look for patterns like:
        - "1 Probability Theory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1"
        - "2 Distribution Theory and Statistical Models . . . . . . . . . . . . . . . . 155"
        - "3 Basic Statistical Theory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 205"

        DO NOT extract lines like:
        - "1.1 Some Important Music Concepts . . . . . . . . . . . 3"
        - "Preface . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . v"

        Use ONLY the exact titles from the document. Do not shorten or modify them.

        Return JSON array: [{{"chapter_number": "X", "chapter_title": "...", "start_page": X, "end_page": X}}]

        REMEMBER: Extract only what is explicitly visible in the text. Do not hallucinate. Be complete and extract all chapters that are clearly numbered.                  y chapters, return an empty array []."""
                },
                {
                    "role": "assistant",
                    "content": "I will carefully examine the table of contents and extract only the main chapters that are explicitly shown, using their exact titles and page numbers. I will not invent or hallucinate any information."
                }
    ]