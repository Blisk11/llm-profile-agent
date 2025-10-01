import sys
from pathlib import Path
import streamlit as st

# Make repo root importable
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.agent import ask_agent
from src.profile_loader import load_profile
from web.components import (
    render_profile_card,
    render_language_selector,
    render_footer,
    display_response,
    render_cv_generator,
    _labels
)

# Example questions database
EXAMPLE_QUESTIONS = {
    "English": [
        "How have you used data analytics to influence a key business decision?",
        "Can you describe a project where you optimized a process or workflow?",
        "How do you approach solving complex problems that combine technical and business challenges?",
        "What demonstrates your entrepreneurial mindset in past professional projects?",
        "Can you show an example of applying AI/ML to generate actionable business insights?"
    ],
    "Français": [
        "Comment avez-vous utilisé l'analyse de données pour influencer une décision clé de l'entreprise ?",
        "Pouvez-vous décrire un projet où vous avez optimisé un processus ou un flux de travail ?",
        "Comment abordez-vous la résolution de problèmes complexes combinant défis techniques et business ?",
        "Qu'est-ce qui démontre votre esprit entrepreneurial dans vos projets professionnels passés ?",
        "Pouvez-vous donner un exemple d'application de l'IA/ML pour générer des insights exploitables ?"
    ]
}

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

def render_question_form(labels: dict, on_submit) -> str:
    """Render the question input form"""
    with st.form(key="question_form"):
        question = st.text_area(
            labels["free_question_placeholder"],
            key="free_question_input",
            height=150
        )
        submit_button = st.form_submit_button(labels["free_button"])
        
        if submit_button and question.strip():
            return on_submit(question)
    return None

def render_example_questions(labels: dict, questions: dict, lang: str, on_submit) -> str:
    """Render example questions with radio buttons"""
    st.markdown(labels["example_header"])
    
    # Use radio buttons for example questions
    selected = st.radio(
        labels["example_dropdown"],
        questions[lang],
        key="example_questions",
        label_visibility="collapsed"  # Hides the label since we use markdown header
    )
    
    if st.button(labels["example_button"], key="example"):
        return on_submit(selected)
    return None

def render_conversation_history(history: list, labels: dict):
    """Render conversation history chronologically"""
    if not history:
        return
    
    st.markdown("### Previous Conversations")
    
    for i, entry in enumerate(history):
        with st.expander(f"Q{i+1}: {entry['question'][:100]}...", expanded=False):
            st.markdown("**Question:**")
            st.markdown(entry['question'])
            st.markdown("**Response:**")
            st.markdown(entry['response'])
            st.markdown(f"*Mode: {entry['mode']} | Language: {entry['lang']}*")
    
    # Add download button
    conversation_text = "\n\n".join([
        f"Q: {turn['question']}\nA: {turn['response']}"
        for turn in history
    ])
    st.download_button(
        labels["download_transcript"],
        data=conversation_text,
        file_name="conversation.txt",
        mime="text/plain"
    )

def main():
    # Language and mode selection
    lang, mode = render_language_selector()
    
    # Get localized labels
    labels = _labels(lang)
    
    # Page configuration
    st.set_page_config(
        page_title=f"Julien Vaughan — {labels['title']}",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Load profile and render profile card
    profile = load_profile()
    with st.sidebar:
        render_cv_generator(ask_agent)
        if profile:
            render_profile_card(profile, lang, expanded=False)

    # Define callback for question submission
    def handle_question(question: str) -> str:
        with st.spinner(labels["spinner_thinking"]):
            response = ask_agent(question, mode=mode)
            if response:
                # Store in session history
                st.session_state.history.append({
                    "question": question,
                    "response": response,
                    "mode": mode,
                    "lang": lang,
                    "timestamp": st.session_state.get("_current_time", "")
                })
            return response

    # Main layout
    st.markdown(f"### {labels['title']}")
    st.markdown("---")
    
    # Two-column layout for questions
    col1, col2 = st.columns([1, 2.5])
    
    with col1:
        st.markdown(labels["free_question_header"])
        response = render_question_form(labels, handle_question)
    
    with col2:
        example_response = render_example_questions(
            labels,
            EXAMPLE_QUESTIONS,
            lang,
            handle_question
        )
    
    # Display current response
    response = response or example_response
    if response:
        st.markdown("### Current Response")
        display_response(response, agent_label=labels["agent"], as_markdown=True)
    
    # Display conversation history
    render_conversation_history(st.session_state.history, labels)
    
    # Footer
    render_footer()

if __name__ == "__main__":
    main()
