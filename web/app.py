import sys
from pathlib import Path
import streamlit as st

# make repo root importable
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.agent import ask_agent
from src.profile_loader import load_profile
from web.components import (
    render_profile_card, 
    display_response, 
    transcript_download_button, 
    load_profile_from_path
)

# Define labels/translations
labels = {
    "English": {
        "title": "Julien Vaughan — Professional Profile Agent",
        "free_question_header": "Ask me anything",
        "free_question_placeholder": "Enter your question here...",
        "free_button": "Ask",
        "example_header": "Or try these example questions:",
        "example_dropdown": "Select a question:",
        "example_button": "Ask selected",
        "answer_label": "Answer",
        "spinner_thinking": "Thinking...",
        "agent": "Julien"  # Added agent label
    },
    "Français": {
        "title": "Julien Vaughan — Agent profil professionnel",
        "free_question_header": "Posez-moi une question",
        "free_question_placeholder": "Entrez votre question ici...",
        "free_button": "Demander",
        "example_header": "Ou essayez ces exemples :",
        "example_dropdown": "Sélectionnez une question :",
        "example_button": "Demander",
        "answer_label": "Réponse",
        "spinner_thinking": "Réflexion en cours...",
        "agent": "Julien"  # Added agent label
    }
}

# --- Sidebar: Language & Answer Mode ---
with st.sidebar:
    lang = st.radio("Langue / Language", ["Français", "English"])
    mode_options = ["Court", "Long"] if lang == "Français" else ["Short", "Long"]
    mode_label = "Mode de réponse" if lang == "Français" else "Answer Mode"
    mode = st.radio(mode_label, mode_options, index=0)
    mode_value = "short" if mode in ["Short", "Court"] else "long"

# --- Streamlit page config ---
st.set_page_config(
    page_title=labels[lang]["title"],
    layout="wide",
    initial_sidebar_state="expanded"  # Changed from "collapsed" to "expanded"
)

# Get localized labels
L = labels[lang]

# --- Page Layout ---
st.markdown(f"### {L['title']}")  # Changed from st.title() to st.markdown() with h3
st.markdown("---")
col1, col2 = st.columns([0.7, 2])

response = None  # Store response here

# --- Free Question Column ---
with col1:
    st.markdown(L["free_question_header"])
    free_question = st.text_area(L["free_question_placeholder"], height=200)
    if st.button(L["free_button"], key="free"):
        if free_question.strip():
            with st.spinner(L["spinner_thinking"]):
                response = ask_agent(free_question, mode=mode_value)

# --- Example Question Column ---
with col2:
    st.markdown(L["example_header"])
    example_questions = {
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
    selected_question = st.radio(L["example_dropdown"], example_questions[lang])
    if st.button(L["example_button"], key="example"):
        with st.spinner(L["spinner_thinking"]):
            response = ask_agent(selected_question, mode=mode_value)

# --- Display Response ---
if response:
    display_response(
        response,
        agent_label=L["agent"],
        as_markdown=True,
        expanded=True
    )
