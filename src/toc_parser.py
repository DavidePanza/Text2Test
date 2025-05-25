from runpod_client import format_messages_as_prompt, run_prompt, clean_and_parse_json
from messages_templates import get_toc_extraction_messages

def extract_chapters_from_toc(toc_text: str):
    messages = get_toc_extraction_messages(toc_text)
    prompt = format_messages_as_prompt(messages)
    raw_output = run_prompt(prompt)
    return clean_and_parse_json(raw_output)