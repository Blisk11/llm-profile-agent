# web/components.py
import streamlit as st

def display_profile(profile, title="Profile Summary", expanded=False):
    """
    Display a profile dictionary in a collapsible container.
    """
    with st.expander(title, expanded=expanded):
        st.json(profile)

def display_response(response, agent_label="Agent", as_markdown=True, expanded=True):
    """
    Display the agent's response.
    - as_markdown: if True, render using Markdown; else render as plain text.
    - expanded: if True, show in a collapsible container.
    """
    container_title = agent_label  # use the label exactly as provided
    if expanded:
        with st.expander(container_title, expanded=True):
            if as_markdown:
                st.markdown(response)
            else:
                st.text(response)
    else:
        if as_markdown:
            st.markdown(f"**{agent_label}:** {response}")
        else:
            st.text(f"{agent_label}: {response}")
