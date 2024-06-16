import streamlit as st
from utils.serpapi_utils import get_google_search_results
from utils.scraping_utils import scrape_text_from_url
from utils.chat_utils import generate_seo_brief, improve_brief
from components.sidebar import render_sidebar
from components.generate_brief import generate_brief_section
from components.improve_brief import improve_brief_section

# Initialize session state
if "generated_brief" not in st.session_state:
    st.session_state["generated_brief"] = ""
if "improvement_messages" not in st.session_state:
    st.session_state["improvement_messages"] = []

# Sidebar for API key input and configuration
render_sidebar()

# Phase 1: Initial Brief Generation
generate_brief_section()

# Phase 2: Interactive Improvement
improve_brief_section()
