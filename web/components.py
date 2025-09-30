import streamlit as st

def display_profile(profile):
    st.subheader("Profile Summary")
    st.json(profile)

def display_response(response):
    st.markdown(f"**Agent:** {response}")
