import streamlit as st


def show_questions():
    """
    Displays the generated questions in a scrollable format.
    """
    for idx, question_item in enumerate(st.session_state['questions_json']):
        question_text = question_item['question']
        answer_text = question_item['answer']

        col1, col2 = st.columns([0.9, 0.1])
        
        with col1:
            st.html(f"<p style='font-size:20px; margin:0;'>{idx+1}. {question_text}</p>")
            col1_ = st.columns([1, 4])[0]
            with col1_:
                with st.expander("💡 Show Answer"):
                    st.write(answer_text)

        with col2:
            selected = st.checkbox("📌", key=f"select_{idx}", value=True)