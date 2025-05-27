from app.backend.runpod_client import format_messages_as_prompt, run_prompt, clean_and_parse_json
from app.backend.messages_templates import toc_prompt
import streamlit as st

def extract_chapters_from_toc(toc_text: str):
    prompt = toc_prompt(toc_text)
    # prompt = format_messages_as_prompt(messages) get rid of this
    print("use prompt optimized for gemma3")
    raw_output = run_prompt(prompt)
    st.session_state['chapters_dict'] = clean_and_parse_json(raw_output)