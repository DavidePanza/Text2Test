import streamlit as st
from app.utils import debug_log


def show_questions(questons_to_show):
    """
    Displays the generated questions in a scrollable container-style format.
    """
    with st.container():
        st.markdown("### Generated Questions")
        st.markdown("---")  # Optional visual separator
        if not questons_to_show:
            debug_log("No questions to display.")
            return
    
        for idx, question_item in enumerate(questons_to_show):
            question_text = question_item['question']
            answer_text = question_item['answer']

            col1, col2 = st.columns([0.9, 0.1])
            
            with col1:
                st.html(f"<p style='font-size:18px; margin:0;'>{idx+1}. {question_text}</p>")
                col1_ = st.columns([2, 3])[0]
                with col1_:
                    with st.expander("💡 Show Answer"):
                        st.write(answer_text)

            with col2:
                st.checkbox("📌", key=f"select_{idx}", value=True)

            st.markdown("")


def sync_selected_questions_to_download(chapter_or_query, questions_dict):
    """Syncs checked questions to the download list."""
    if chapter_or_query is None:
        st.error("No chapter or query selected!")
        return

    if chapter_or_query not in st.session_state['questions_to_download']:
        st.session_state['questions_to_download'][chapter_or_query] = []

    current_selected = st.session_state['questions_to_download'][chapter_or_query]

    for idx, question in enumerate(questions_dict):
        current_question = {'question': question['question'], 'answer': question['answer']}
        checkbox_key = f"select_{idx}"
        is_selected = st.session_state.get(checkbox_key, False)

        if is_selected and current_question not in current_selected:
            current_selected.append(current_question)
        elif not is_selected and current_question in current_selected:
            current_selected.remove(current_question)

    st.success(f"Selected questions synced for chapter or query '{chapter_or_query}'.")


def clear_selected_questions():
    """Clears all selected questions from session state."""
    st.session_state['questions_to_download'] = {}
    st.success("Cleared all selected questions.")


def show_download_controls(chapter_or_query, questions_dict):
    """Displays buttons to sync or clear selected questions."""
    col1_download, col2_download, _ = st.columns([0.3, 0.3, 0.4])

    with col1_download:
        if st.button("Sync Selected Questions to Download"):
            sync_selected_questions_to_download(chapter_or_query, questions_dict)

    with col2_download:
        if st.button("Clear Selected Questions"):
            clear_selected_questions()


def debug_show_selected_questions():
    """Debug printout of currently selected questions per chapter."""
    if st.session_state.get('questions_to_download'):
        debug_log("✅ Selected Questions")
        for chapter, questions_list in st.session_state['questions_to_download'].items():
            debug_log(f"{chapter}")
            for q in questions_list:
                debug_log(q['question'])