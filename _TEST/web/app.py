# File: web/app.py
"""
Refactored Streamlit app that uses the components module above.
- Centralized labels and translations
- Cleaner separation: app handles state & orchestration, components handle presentation
- Uses st.session_state to persist the last response
"""
import sys
from pathlib import Path
import streamlit as st

# make repo root importable (keeps the existing project layout working)
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.agent import ask_agent
from src.profile_loader import load_profile_only as _load_profile
from web.components import render_profile_card, display_response, transcript_download_button, load_profile_from_path

# --- Page config ---
st.set_page_config(page_title="Julien Vaughan — Personal Agent", layout="wide")

# --- Translations for app-level strings ---
APP_LABELS = {
    "English": {
        "title": "Julien Vaughan — Personal Agent",
        "free_question_header": "Free question",
        "free_question_placeholder": "Type your question here (e.g. 'How did Julien impact revenue in project X?')",
        "free_button": "Ask",
        "example_header": "Example questions",
        "example_dropdown": "Pick an example:",
        "example_button": "Ask example",
        "answer_label": "Agent response",
        "spinner_thinking": "Thinking...",
        "view_profile": "View profile",
        "download_transcript": "Download conversation"
    },
    "Français": {
        "title": "Agent Personnel — Julien Vaughan",
        "free_question_header": "Question libre",
        "free_question_placeholder": "Tapez votre question ici (ex: 'Comment Julien a impacté le CA sur le projet X ?')",
        "free_button": "Poser",
        "example_header": "Questions d'exemple",
        "example_dropdown": "Choisissez un exemple :",
        "example_button": "Poser l'exemple",
        "answer_label": "Réponse",
        "spinner_thinking": "Réflexion en cours...",
        "view_profile": "Voir le profil",
        "download_transcript": "Télécharger la conversation"
    }
}

# --- Sidebar: language and mode ---
with st.sidebar:
    lang = st.radio("Langue / Language", ["Français", "English"], index=0)
    mode_options = ["Court", "Long"] if lang == "Français" else ["Short", "Long"]
    mode_label = "Mode de réponse" if lang == "Français" else "Answer mode"
    mode = st.radio(mode_label, mode_options, index=0)
    mode_value = "short" if mode in ["Short", "Court"] else "long"

L = APP_LABELS[lang]

# --- Load profile (try src.profile_loader, else fallback to data/profile.json) ---
try:
    profile = _load_profile()
except Exception:
    profile = load_profile_from_path(str(ROOT / "data" / "profile.json"))

# --- Page layout ---
st.title(L["title"])
st.markdown("---")
col_left, col_right = st.columns([1, 2.5])

# left: profile card + examples
with col_left:
    if st.checkbox(L.get("view_profile", "View profile"), value=True):
        render_profile_card(profile, lang=lang)

    st.markdown(L["example_header"])
    example_questions = {
        "English": [
            "How have you used data analytics to influence a key business decision?",
            "Describe a project where you optimized a process or workflow.",
            "How do you approach solving complex problems that combine technical and business challenges?",
            "What demonstrates your entrepreneurial mindset in past professional projects?",
            "Give an example where AI/ML produced actionable business insights."
        ],
        "Français": [
            "Comment avez-vous utilisé l'analyse de données pour influencer une décision clé ?",
            "Décrivez un projet où vous avez optimisé un processus ou un flux de travail.",
            "Comment abordez-vous la résolution de problèmes techniques et business ?",
            "Qu'est-ce qui démontre votre esprit entrepreneurial dans vos projets ?",
            "Donnez un exemple d'application IA/ML produisant des insights exploitables."
        ]
    }

    selected_question = st.selectbox(L["example_dropdown"], example_questions[lang])
    if st.button(L["example_button"], key="example"):
        if selected_question:
            with st.spinner(L["spinner_thinking"]):
                st.session_state.response = ask_agent(selected_question, mode=mode_value)

# right: free question and answer
with col_right:
    st.markdown(L["free_question_header"])
    free_question = st.text_area(L["free_question_placeholder"], height=180, key="free_question")
    if st.button(L["free_button"], key="ask_free"):
        q = free_question.strip()
        if q:
            with st.spinner(L["spinner_thinking"]):
                st.session_state.response = ask_agent(q, mode=mode_value)

    # Display previous response if present in session state
    response = st.session_state.get("response")
    if response:
        st.markdown("---")
        display_response(response, agent_label=L.get("answer_label"), as_markdown=True, expanded=True)

        # download button for transcript
        transcript_text = f"Question:\n{st.session_state.get('free_question','(example)')}\n\nResponse:\n{response}\n"
        transcript_download_button(transcript_text, filename="julien_agent_conversation.txt", label=L.get("download_transcript"))

# Footer: a small hint for maintainers
st.markdown("---")
st.caption("Technical notes: app keeps UI and presentation in web/components.py and logic in src/. Use `streamlit run web/app.py` to run locally.")
