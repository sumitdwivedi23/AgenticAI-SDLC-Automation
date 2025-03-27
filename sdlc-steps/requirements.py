import streamlit as st

def get_requirements():
    """Collect requirements from the user via Streamlit UI."""
    st.header("Enter Software Requirements")
    requirements = st.text_area("Please provide your software requirements:", height=200)
    return requirements