# web/app.py
import streamlit as st
from src import ask_agent
from web.components import display_response

# --- Streamlit page config ---
st.set_page_config(page_title="Julien Vaughan Personal Agent", layout="wide")

# --- Sidebar: language and response mode ---
with st.sidebar:
    lang = st.radio("Langue / Language", ["Français", "English"])
    mode_options = ["Short", "Long"] if lang == "English" else ["Court", "Long"]
    mode_label = "Answer Mode" if lang == "English" else "Mode de réponse"
    mode = st.radio(mode_label, mode_options, index=0)
    mode_value = "short" if mode in ["Short", "Court"] else "long"

# --- Labels based on language ---
labels = {
    "English": {
        "title": "Julien Vaughan Personal Agent",
        "free_header": "### Free Question",
        "free_placeholder": "Type your question here",
        "free_button": "Submit Free Question",
        "example_header": "### Example Questions",
        "example_dropdown": "Select an example question:",
        "example_button": "Ask Selected Question",
        "answer": "Agent",
    },
    "Français": {
        "title": "Agent Personnel de Julien Vaughan",
        "free_header": "### Question Libre",
        "free_placeholder": "Tapez votre question ici",
        "free_button": "Poser la question",
        "example_header": "### Questions d'exemple",
        "example_dropdown": "Sélectionnez une question d'exemple :",
        "example_button": "Poser la question sélectionnée",
        "answer": "Réponse",
    }
}

l = labels[lang]
st.title(l["title"])
st.markdown("---")

# --- Layout columns ---
col1, col2 = st.columns([0.7, 2])
response = None

# --- Free question input ---
with col1:
    st.markdown(l["free_header"])
    free_question = st.text_area(l["free_placeholder"], height=200)
    if st.button(l["free_button"], key="free"):
        if free_question.strip():
            with st.spinner("Thinking..."):
                response = ask_agent(free_question, mode=mode_value)

# --- Example questions ---
with col2:
    st.markdown(l["example_header"])
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
    selected_question = st.radio(l["example_dropdown"], example_questions[lang])
    if st.button(l["example_button"], key="example"):
        with st.spinner("Thinking..."):
            response = ask_agent(selected_question, mode=mode_value)

# --- Show response below both columns ---
if response:
    st.markdown("---")
    display_response(response, agent_label=l["answer"])
