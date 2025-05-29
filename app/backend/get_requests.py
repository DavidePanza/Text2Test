from app.backend.runpod_client import format_messages_as_prompt, run_prompt, clean_and_parse_json
from app.backend.messages_templates import toc_prompt, chapter_prompt, chapter_prompt_edgecase
import streamlit as st


def extract_chapters_from_toc(toc_text: str):
    prompt = toc_prompt(toc_text)
    # prompt = format_messages_as_prompt(messages) get rid of this
    print("use prompt optimized for gemma3")
    raw_output = run_prompt(prompt)
    st.session_state['chapters_dict'] = clean_and_parse_json(raw_output)


def generate_questions_from_chapter(chunks, num_questions, max_questions=5):
    prompt = chapter_prompt(contexts=chunks, num_questions=num_questions, max_questions=max_questions)
    # prompt = format_messages_as_prompt(messages) get rid of this
    print("use prompt optimized for gemma3")
    raw_output = run_prompt(prompt)
    try:
        st.session_state['questions_json'] = clean_and_parse_json(raw_output)
        st.success("Questions generated successfully!")
    except:
        print("Error parsing JSON, using raw output instead.")
    return raw_output # Return raw output for debugging


def generate_questions_from_chapter_edgecase(chunks, num_questions, max_questions=5):
    prompt = chapter_prompt_edgecase(grouped_chunks=chunks, num_questions=num_questions, max_questions=max_questions)
    # prompt = format_messages_as_prompt(messages) get rid of this
    print("use prompt optimized for gemma3")
    raw_output = run_prompt(prompt)
    try:
        st.session_state['questions_json'] = clean_and_parse_json(raw_output)
        st.success("Questions generated successfully!")
    except:
        print("Error parsing JSON, using raw output instead.")
    return raw_output # Return raw output for debugging