from runpod_client import format_messages_as_prompt, run_prompt, clean_and_parse_json
from messages_templates import toc_prompt

def extract_chapters_from_toc(toc_text: str):
    prompt = toc_prompt(toc_text)
    # prompt = format_messages_as_prompt(messages) get rid of this
    print("use prompt optimized for gemma3")
    raw_output = run_prompt(prompt)
    return clean_and_parse_json(raw_output)