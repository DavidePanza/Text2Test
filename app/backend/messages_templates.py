# def get_toc_extraction_messages(toc_text: str):
#     return [
#         {
#             "role": "system",
#             "content": "You are a precise document parser that extracts structured information from table of contents. You NEVER hallucinate You NEVER hallucinate, invent, or make up information. You ONLY extract what is explicitly present in the provided text. If you cannot find clear chapter information, you return an empty array. You do not guess chapter titles or page numbers."
#         },
#         {
#             "role": "user",
#             "content": "I need to extract main chapter information from this table of contents. Only extract numbered chapters, ignore subsections. Do not make up any information."
#         },
#         {
#             "role": "assistant",
#             "content": "I understand. I will extract ONLY the main chapters that are explicitly shown in your table of contents. I will not invent, guess, or hallucinate any chapter titles or page numbers. I will only use the exact information present in the document."
#         },
#         {
#             "role": "user",
#             "content": f"""Here is the table of contents:

#         {toc_text}

#         WARNING: DO NOT HALLUCINATE OR INVENT INFORMATION
#         - Do NOT make up chapter titles like "Probability", "Statistical Inference", "Linear Regression"
#         - Do NOT guess page numbers
#         - Do NOT create generic textbook chapters
#         - ONLY extract what you can clearly see in the provided text

#         CRITICAL RULES:
#         1. Extract ONLY main chapters that start with a number (1, 2, 3, etc.)
#         2. Do NOT extract subsections (like 1.1, 1.2, 2.1, etc.)
#         3. Use the EXACT chapter titles shown in the document
#         4. Use the EXACT page numbers shown in the document
#         5. Handle both roman numerals (i, ii, iii, v, x) and arabic numerals (1, 25, 100)
#         6. Calculate end pages as: next chapter's start page minus 1
#         7. Return ONLY valid JSON - no explanations, no markdown formatting
#         8. If you cannot clearly identify chapters, return empty array []

#         Look for patterns like:
#         - "1 Probability Theory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1"
#         - "2 Distribution Theory and Statistical Models . . . . . . . . . . . . . . . . 155"
#         - "3 Basic Statistical Theory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 205"

#         DO NOT extract lines like:
#         - "1.1 Some Important Music Concepts . . . . . . . . . . . 3"
#         - "Preface . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . v"

#         Use ONLY the exact titles from the document. Do not shorten or modify them.

#         Return JSON array: [{{"chapter_number": "X", "chapter_title": "...", "start_page": X, "end_page": X}}]

#         REMEMBER: Extract only what is explicitly visible in the text. Do not hallucinate. Be complete and extract all chapters that are clearly numbered.                  y chapters, return an empty array []."""
#                 },
#                 {
#                     "role": "assistant",
#                     "content": "I will carefully examine the table of contents and extract only the main chapters that are explicitly shown, using their exact titles and page numbers. I will not invent or hallucinate any information."
#                 }
#     ]


def toc_prompt(toc_text: str):
    # Convert to Gemma 3 format - single string with proper turn markers
    prompt = f"""<start_of_turn>user
You are a precise document parser that extracts structured information from table of contents. You NEVER hallucinate, invent, or make up information. You ONLY extract what is explicitly present in the provided text. If you cannot find clear chapter information, you return an empty array.

I need to extract main chapter information from this table of contents. Only extract numbered chapters, ignore subsections. Do not make up any information.

Here is the table of contents:

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
- "Preface . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . v"

Use ONLY the exact titles from the document. Do not shorten or modify them.

Return JSON array: [{{"chapter_number": "X", "chapter_title": "...", "start_page": X, "end_page": X}}]

Extract only what is explicitly visible in the text. Do not hallucinate. Be complete and extract all chapters that are clearly numbered. If no clear main chapters, return an empty array [].<end_of_turn>
<start_of_turn>model
I will carefully examine the table of contents and extract only the main chapters that are explicitly shown, using their exact titles and page numbers. I will not invent or hallucinate any information.

Looking at the provided table of contents, I will now extract the main chapters:<end_of_turn>
<start_of_turn>user
Perfect. Now provide the JSON array with the extracted chapters.<end_of_turn>
<start_of_turn>model
"""
    
    return prompt


def chapter_prompt(contexts, num_questions, max_questions=5):
    """
    Create a prompt formatted for Gemma 3 12B-IT model.
    This prompt is designed to generate diverse questions based on provided text contexts.
    Args:
        contexts (list): List of text contexts to base questions on.
        num_questions (int): Number of questions to generate.
        max_questions (int): Maximum number of questions allowed.  
    Returns:
        str: Formatted prompt string for Gemma 3 model.
    """
    
    # Gemma uses special tokens for instruction tuning
    prompt = """<start_of_turn>user
You are a question generation expert. Generate exactly {num_questions} diverse questions based on the provided text contexts.

IMPORTANT REQUIREMENTS:
1. Output MUST be valid JSON format
2. Generate EXACTLY {num_questions} questions
3. Each question must have a complete answer from the contexts
4. Vary question types (what, why, how, when, explain, compare)
5. Do not generate yes/no questions
6. Answers should be 1-3 sentences long

CONTEXTS:
{contexts}

OUTPUT FORMAT - Return ONLY valid JSON array:
[
{{"question": "Your question here?", "answer": "Complete answer from the context"}},
{{"question": "Another question?", "answer": "Another answer"}}
]

Generate the questions now:<end_of_turn>
<start_of_turn>model
""".format(
        num_questions=min(num_questions, max_questions),
        contexts=format_contexts(contexts)
    )
    
    return prompt

def chapter_prompt_edgecase(grouped_chunks, num_questions, max_questions=5):
    """
    Create a prompt formatted for Gemma 3 12B-IT model.
    This prompt is designed to handle edge cases where contexts retrieved are less than the number of questions requested.
    Args:
        contexts (list): List of text contexts to format.
    Returns:
        str: Formatted string of contexts.
    """
    
    prompt = """<start_of_turn>user
Generate {num_questions} questions from the following contexts. You may:
- Generate one or more questions from each context
- Use multiple contexts for a single question
- Skip contexts if they don't contain meaningful information

REQUIREMENTS:
1. Output valid JSON array format
2. Generate EXACTLY {num_questions} questions
3. Each answer must be found in the provided contexts
4. Create diverse question types
5. Reference which context group(s) you used

CONTEXT GROUPS:
{context_groups}

OUTPUT FORMAT - Return ONLY this JSON structure:
[
{{"question": "Question text?", "answer": "Answer text", "context_used": [1, 2]}},
{{"question": "Question text?", "answer": "Answer text", "context_used": [1]}}
]

Generate the questions:<end_of_turn>
<start_of_turn>model
""".format(
        num_questions=min(num_questions, max_questions),
        context_groups=format_contexts(grouped_chunks)
    )
    
    return prompt


def book_prompt(contexts, num_questions, user_query=None, max_questions=5):
    """
    Create a prompt formatted for Gemma 3 12B-IT model with topic awareness.
    
    Args:
        contexts (list): List of text contexts retrieved based on user query
        num_questions (int): Number of questions to generate
        user_query (str): The original user query/topic
        max_questions (int): Maximum number of questions allowed
    
    Returns:
        str: Formatted prompt string for Gemma 3 model
    """
    
    num_questions = min(num_questions, max_questions)
    
    # Build topic context section if query provided
    topic_context = ""
    if user_query:
        topic_context = f"""
TOPIC FOCUS: {user_query}
The following contexts were retrieved based on this topic. Generate questions that:
- Relate to the main topic: "{user_query}"
- Explore different aspects of this topic found in the contexts
- Connect the topic to broader concepts when relevant

"""
    
    prompt = """<start_of_turn>user
You are a question generation expert. Generate exactly {num_questions} diverse questions based on the provided text contexts.
{topic_context}
IMPORTANT REQUIREMENTS:
1. Output MUST be valid JSON format
2. Generate EXACTLY {num_questions} questions
3. Each question must have a complete answer from the contexts
4. Vary question types (what, why, how, when, explain, compare)
5. Do not generate yes/no questions
6. Answers should be 1-3 sentences long
7. Questions should explore different aspects of the topic

CONTEXTS (Retrieved based on topic: "{query}"):
{contexts}

OUTPUT FORMAT - Return ONLY valid JSON array:
[
{{"question": "Your question here?", "answer": "Complete answer from the context"}},
{{"question": "Another question?", "answer": "Another answer"}}
]

Generate the questions now:<end_of_turn>
<start_of_turn>model
""".format(
        num_questions=num_questions,
        topic_context=topic_context,
        query=user_query if user_query else "the provided content",
        contexts=format_contexts(contexts)
    )
    
    return prompt


def format_contexts(contexts):
    """
    Format contexts for better readability.
    """
    formatted = ""
    for i, context in enumerate(contexts, 1):
        formatted += f"Context {i}:\n{context.strip()}\n\n"
    return formatted.strip()

