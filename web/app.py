import sys
import os

# Ensure src is on the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agent import ask_agent
import streamlit as st
from web.components import display_response

# --- Streamlit page config ---
st.set_page_config(page_title="Julien Vaughan Personal Agent", layout="wide")

# --- Sidebar: Language & Answer Mode ---
with st.sidebar:
    lang = st.radio("Langue / Language", ["Français", "English"])
    mode_options = ["Court", "Long"] if lang == "Français" else ["Short", "Long"]
    mode_label = "Mode de réponse" if lang == "Français" else "Answer Mode"
    mode = st.radio(mode_label, mode_options, index=0)
    mode_value = "short" if mode in ["Short", "Court"] else "long"

# --- Bilingual Labels ---
labels = {
    "English": {
        "title": "Julien Vaughan Personal Agent",
        "free_question_header": "### Free Question",
        "free_question_placeholder": "Type your question here",
        "free_button": "Submit Free Question",
        "example_header": "### Example Questions",
        "example_dropdown": "Select an example question:",
        "example_button": "Ask Selected Question",
        "answer_label": "Agent Response",
        "spinner_thinking": "Thinking..."
    },
    "Français": {
        "title": "Agent Personnel de Julien Vaughan",
        "free_question_header": "### Question Libre",
        "free_question_placeholder": "Tapez votre question ici",
        "free_button": "Poser la question",
        "example_header": "### Questions d'exemple",
        "example_dropdown": "Sélectionnez une question d'exemple :",
        "example_button": "Poser la question sélectionnée",
        "answer_label": "Réponse",
        "spinner_thinking": "Réflexion en cours..."
    }
}

L = labels[lang]

# --- Page Layout ---
st.title(L["title"])
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
    st.markdown("---")
    display_response(response, agent_label=L["answer_label"], expanded=True)
