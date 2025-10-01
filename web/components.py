# File: web/components.py
"""
Refactored UI components for the Streamlit agent.
This module focuses purely on presentation and small UI helpers.
Keep translations here so app.py stays very small.
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
import streamlit as st


def _labels(lang: str = "English") -> Dict[str, str]:
    return {
        "English": {
            "title": "Julien Vaughan — Professional Profile Agent",
            "profile_title": "Profile",
            "skills": "Skills",
            "contact": "Contact",
            "view_raw": "View raw profile (JSON)",
            "download_transcript": "Download conversation",
            "no_profile": "No profile data available",
            "agent": "Agent",
            "free_question_header": "Ask a free question",
            "free_question_placeholder": "Type your question here...",
            "free_button": "Submit",
            "example_header": "Or try one of these questions:",
            "example_dropdown": "Select a question",
            "spinner_thinking": "Thinking...",
            "example_button": "Ask",
        },
        "Français": {
            "title": "Julien Vaughan — Agent profil professionnel",
            "profile_title": "Profil",
            "skills": "Compétences",
            "contact": "Contact",
            "view_raw": "Voir le profil brut (JSON)",
            "download_transcript": "Télécharger la conversation",
            "no_profile": "Aucune donnée de profil disponible",
            "agent": "Agent",
            "free_question_header": "Posez une question libre",
            "free_question_placeholder": "Tapez votre question ici...",
            "free_button": "Soumettre",
            "example_header": "Ou essayez l'une de ces questions :",
            "example_dropdown": "Sélectionnez une question",
            "example_button": "Demander",
            "spinner_thinking": "Réflexion en cours...",
        }
    }[lang]


def render_profile_card(profile: Optional[Dict[str, Any]], lang: str = "English", expanded: bool = True) -> None:
    """Render a compact, recruiter-friendly profile card.
    Optimized for sidebar display with single column layout.
    """
    L = _labels(lang)

    if not profile:
        st.info(L["no_profile"])
        return

    # Main card in a single column
    with st.container():

        # Contact info with better spacing
        contact = profile.get("contact") or {}
        if isinstance(contact, dict) and any(contact.values()):
            st.markdown("---")
            st.markdown(f"**{L['contact']}**")
            if contact.get("email"):
                st.markdown(f"📧 {contact['email']}")
            if contact.get("phone"):
                st.markdown(f"📱 {contact['phone']}")
            if contact.get("linkedin"):
                st.markdown(f"🔗 [{L.get('linkedin', 'LinkedIn')}]({contact['linkedin']})")
            if contact.get("address"):
                st.markdown(f"📍 {contact['address']}")


def display_response(response: str, agent_label: Optional[str] = None, as_markdown: bool = True, expanded: bool = True) -> None:
    """Display the agent response in a readable container.

    - If expanded: show inside an expander with the agent label.
    - If not expanded: show inline with a small header.
    """
    label = agent_label or _labels()["agent"]
    if expanded:
        with st.expander(label, expanded=True):
            if as_markdown:
                st.markdown(response)
            else:
                st.text(response)
    else:
        st.subheader(label)
        if as_markdown:
            st.markdown(response)
        else:
            st.text(response)


def transcript_download_button(text: str, filename: str = "conversation.txt", label: Optional[str] = None) -> None:
    """Provide a download button for the conversation/transcript.

    - Keeps the UI code isolated and reusable.
    """
    if label is None:
        label = _labels()["download_transcript"]
    st.download_button(label, data=text, file_name=filename, mime="text/plain")


# Small helper used by the app when profile.json is present on disk
def load_profile_from_path(path: str) -> Optional[Dict[str, Any]]:
    try:
        p = Path(path)
        if not p.exists():
            return None
        import json
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None

def render_language_selector() -> tuple[str, str]:
    """Render language and mode selection in sidebar"""
    lang = st.sidebar.radio("Langue / Language", ["Français", "English"])
    mode_options = ["Court", "Long"] if lang == "Français" else ["Short", "Long"]
    mode_label = "Mode de réponse" if lang == "Français" else "Answer Mode"
    mode = st.sidebar.radio(mode_label, mode_options, index=0)
    mode_value = "short" if mode in ["Short", "Court"] else "long"
    return lang, mode_value

def render_question_input(labels: dict, on_submit) -> str:
    """Render the free question input area"""
    st.markdown(labels["free_question_header"])
    question = st.text_area(
        labels["free_question_placeholder"],
        key="free_question_input",
        height=300
    )
    if st.button(labels["free_button"], key="free"):
        if question.strip():
            return on_submit(question)
    return None

def render_example_questions(labels: dict, questions: dict, lang: str, on_submit) -> str:
    """Render example questions selection"""
    st.markdown(labels["example_header"])
    selected = st.radio(
        labels["example_dropdown"],
        questions[lang],
        key="example_questions"
    )
    if st.button(labels["example_button"], key="example"):
        return on_submit(selected)
    return None

def render_conversation_history(conversation: list, lang: str):
    """Render conversation history and download button"""
    if not conversation:
        return
        
    conversation_text = "\n\n".join([
        f"Q: {turn['question']}\nA: {turn['response']}"
        for turn in conversation
    ])
    transcript_download_button(
        text=conversation_text,
        filename=f"conversation_{lang.lower()}.txt"
    )

def render_footer():
    """Render app footer with maintainer info"""
    st.markdown("---")
    st.markdown(
        "🤖 Built with Streamlit + Mistral AI | "
        "[GitHub](https://github.com/Blisk11/llm-profile-agent) | "
        "Maintainer: [Julien Vaughan](https://www.linkedin.com/in/j.vaughan)"
    )