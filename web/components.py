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
            "profile_title": "Profile",
            "skills": "Skills",
            "contact": "Contact",
            "view_raw": "View raw profile (JSON)",
            "download_transcript": "Download conversation",
            "no_profile": "No profile data available",
            "agent": "Agent"
        },
        "Français": {
            "profile_title": "Profil",
            "skills": "Compétences",
            "contact": "Contact",
            "view_raw": "Voir le profil brut (JSON)",
            "download_transcript": "Télécharger la conversation",
            "no_profile": "Aucune donnée de profil disponible",
            "agent": "Agent"
        }
    }[lang]


def render_profile_card(profile: Optional[Dict[str, Any]], lang: str = "English", expanded: bool = True) -> None:
    """Render a compact, recruiter-friendly profile card.

    - Shows name, title, short summary, top skills and contact info.
    - Avoids dumping raw JSON unless the user explicitly asks.
    """
    L = _labels(lang)

    if not profile:
        st.info(L["no_profile"])
        return

    # Main card
    with st.container():
        cols = st.columns([1, 3])
        left, right = cols

        # Left: optional photo
        photo = profile.get("photo") or profile.get("avatar_url")
        if photo:
            try:
                left.image(photo, width=120)
            except Exception:
                left.empty()

        # Right: name, title, summary
        name = profile.get("name") or profile.get("full_name") or ""
        title = profile.get("title") or profile.get("role") or ""
        summary = profile.get("summary") or profile.get("about") or ""

        right.markdown(f"#### {name}")
        if title:
            right.markdown(f"**{title}**")
        if summary:
            right.write(summary)

        # Skills
        skills: List[str] = profile.get("skills") or profile.get("tech_stack") or []
        if skills:
            right.markdown(f"**{L['skills']}:** {', '.join(skills[:10])}")

        # Contact
        contact = profile.get("contact") or {}
        contact_lines = []
        if isinstance(contact, dict):
            if contact.get("email"):
                contact_lines.append(contact.get("email"))
            if contact.get("phone"):
                contact_lines.append(contact.get("phone"))
            if contact.get("linkedin"):
                contact_lines.append(contact.get("linkedin"))
        else:
            # fallback if contact is a string
            if contact:
                contact_lines.append(str(contact))

        if contact_lines:
            right.markdown(f"**{L['contact']}:**  ")
            for c in contact_lines:
                right.write(f"- {c}")

    # optional expander to show raw JSON
    with st.expander(L["view_raw"], expanded=False):
        st.json(profile)


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