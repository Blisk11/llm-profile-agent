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
            "title": "Julien Vaughan – Virtual Application Assistant",
            "profile_title": "Profile",
            "skills": "Skills",
            "contact": "Contact",
            "view_raw": "View raw profile (JSON)",
            "download_transcript": "Download conversation",
            "no_profile": "No profile data available",
            "agent": "Agent",
            "free_question_header": "Ask a free question, for example: ‘Would you be a good candidate for this role?’ (Paste your job description).",
            "free_question_placeholder": "Type your question here...",
            "free_button": "Submit",
            "example_header": "Or try one of these questions:",
            "example_dropdown": "Select a question",
            "spinner_thinking": "Thinking...",
            "example_button": "Ask",
            "generate_cv": "📄 Generate CV",
            "app_description_header": "About this App",
            "app_description_text": (
                "This interactive Streamlit app serves as a professional portfolio "
                "and career showcase. It dynamically generates my profile, highlights "
                "key achievements, technical skills, and projects, and allows you to explore "
                "my portfolio with live links to apps, dashboards, and code repositories."
            ),
            "about_me_header": "About Me",
            "about_me_text": (
                "I am Julien Vaughan, a Business Analyst and Data Scientist with expertise "
                "in Python, SQL, Power BI, and Machine Learning. My work focuses on delivering "
                "data-driven insights, automating business processes, and building analytics solutions "
                "that drive measurable impact for SMEs and larger organizations."
            )
        },
        "Français": {
            "title": "Julien Vaughan – Assistant Virtuel de Candidature",
            "profile_title": "Profil",
            "skills": "Compétences",
            "contact": "Contact",
            "view_raw": "Voir le profil brut (JSON)",
            "download_transcript": "Télécharger la conversation",
            "no_profile": "Aucune donnée de profil disponible",
            "agent": "Agent",
            "free_question_header": "Posez une question libre, par exemple, 'Seriez-vous un bon candidat pour ce poste ?' (Collez votre fiche de poste).",
            "free_question_placeholder": "Tapez votre question ici...",
            "free_button": "Soumettre",
            "example_header": "Ou essayez l'une de ces questions :",
            "example_dropdown": "Sélectionnez une question",
            "spinner_thinking": "Réflexion en cours...",
            "example_button": "Demander",
            "generate_cv": "📄 Générer le CV",
            "app_description_header": "À propos de cette application",
            "app_description_text": (
                "Cette application Streamlit interactive présente un portfolio professionnel "
                "et un profil de carrière. Elle génère dynamiquement mon profil, met en valeur "
                "mes réalisations clés, mes compétences techniques et mes projets, et permet "
                "d'explorer mon portfolio avec des liens actifs vers des applications, dashboards et dépôts de code."
            ),
            "about_me_header": "À propos de moi",
            "about_me_text": (
                "Je suis Julien Vaughan, Business Analyst et Data Scientist spécialisé en Python, SQL, Power BI et Machine Learning. "
                "Mon travail se concentre sur la fourniture d'analyses data-driven, l'automatisation des processus métiers "
                "et la construction de solutions analytiques ayant un impact mesurable pour les PME et les grandes organisations."
            )
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

def render_title(labels: dict):
    st.markdown(f"## {labels['title']}")  # visible H1 title
    st.markdown(labels["app_description_text"])
    st.markdown("---")
    
    # About me section
    st.markdown(f"### {labels['about_me_header']}")
    st.markdown(labels["about_me_text"])
    st.markdown("---")

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
    mode = st.sidebar.radio(mode_label, mode_options, index=1)
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
    

def render_cv_generator(labels: dict, ask_agent):
    """Render a button to generate a CV and show/download it once generated."""

    # Build extra context from conversation history
    history_text = ""
    if "history" in st.session_state and st.session_state.history:
        qa_pairs = [
            f"Q: {turn['question']}\nA: {turn['response']}"
            for turn in st.session_state.history
        ]
        history_text = "\n\n".join(qa_pairs)

    # Button trigger
    if st.button(labels["generate_cv"], key="generate_cv"):
        with st.spinner(labels["spinner_thinking"]):
            cv_prompt = (
                "Using Julien Vaughan's profile, generate a professional, "
                "concise, chronological CV suitable for recruiters. "
                "Format sections as: Contact, Skills, Experience (with achievements), "
                "Education, Languages. Keep it in clean Markdown.\n\n"
            )
            if history_text:
                cv_prompt += (
                    "Here are example questions and responses from recent interactions. "
                    "Incorporate relevant elements where appropriate:\n\n"
                    f"{history_text}"
                )
            cv_text = ask_agent(cv_prompt, mode="long")
            if cv_text:
                st.session_state.cv_text = cv_text
                st.success(labels["generate_cv"] + " ✅")

    # Display generated CV
    if "cv_text" in st.session_state:
        st.markdown("### " + labels["generate_cv"])
        st.markdown(st.session_state.cv_text)
        st.download_button(
            "⬇️ " + labels["generate_cv"],
            data=st.session_state.cv_text,
            file_name="Julien_Vaughan_CV.md",
            mime="text/markdown"
        )

def render_footer():
    """Render app footer with maintainer info"""
    st.markdown("---")
    st.markdown(
        "🤖 Built with Streamlit + Mistral AI | "
        "[GitHub](https://github.com/Blisk11/llm-profile-agent) | "
        "Maintainer: [Julien Vaughan](https://www.linkedin.com/in/j.vaughan)"
    )