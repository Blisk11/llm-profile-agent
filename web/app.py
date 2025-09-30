import sys
import os

# Add src folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import streamlit as st
from src.agent import ask_agent  # import the function directly

st.set_page_config(page_title="Julien Vaughan Personal Agent", layout="wide")

# --- Sidebar for language and answer mode ---
with st.sidebar:
    lang = st.radio("Langue / Language ", ["Français", "English"])
    mode_options = ["Short", "Long"] if lang == "English" else ["Court", "Long"]
    mode_label = "Answer Mode" if lang == "English" else "Mode de réponse"
    mode = st.radio(mode_label, mode_options, index=0)
    mode_value = "short" if mode in ["Short", "Court"] else "long"

# --- Labels based on language ---
if lang == "English":
    title_text = "Julien Vaughan Personal Agent"
    free_question_header = "### Free Question"
    free_question_placeholder = "Type your question here"
    free_button_label = "Submit Free Question"
    example_header = "### Example Questions"
    example_dropdown_label = "Select an example question:"
    example_button_label = "Ask Selected Question"
    answer_label = "**Answer:**"
else:
    title_text = "Agent Personnel de Julien Vaughan"
    free_question_header = "### Question Libre"
    free_question_placeholder = "Tapez votre question ici"
    free_button_label = "Poser la question"
    example_header = "### Questions d'exemple"
    example_dropdown_label = "Sélectionnez une question d'exemple :"
    example_button_label = "Poser la question sélectionnée"
    answer_label = "**Réponse:**"

st.title(title_text)
st.markdown("---")

col1, col2 = st.columns([0.7, 2])

response = None  # Store the response to display below

with col1:
    st.markdown(free_question_header)
    free_question = st.text_area(free_question_placeholder, height=200)
    if st.button(free_button_label, key="free"):
        if free_question.strip():
            with st.spinner("Thinking..."):
                response = ask_agent(free_question, mode=mode_value)

with col2:
    st.markdown(example_header)
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
    selected_question = st.radio(example_dropdown_label, example_questions[lang])
    if st.button(example_button_label, key="example"):
        with st.spinner("Thinking..."):
            response = ask_agent(selected_question, mode=mode_value)

# --- Show response below both columns ---
if response is not None:
    st.markdown("---")
    st.markdown(answer_label)
    st.write(response)
