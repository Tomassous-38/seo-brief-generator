import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.text_input("Anthropic API Key", key="chatbot_api_key", type="password")
        st.text_input("SerpAPI Key", key="serpapi_key", type="password")
        
        st.selectbox(
            "Select Model",
            [
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307",
                "claude-2.1",
                "claude-2.0",
                "claude-instant-1.2"
            ]
        )
        st.slider("Select Temperature", 0.0, 1.0, 0.0, 0.1)
        st.number_input("Max Tokens", min_value=1, max_value=4000, value=1024)
