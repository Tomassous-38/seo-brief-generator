import streamlit as st
from utils.serpapi_utils import get_google_search_results
from utils.scraping_utils import scrape_text_from_url
from utils.chat_utils import generate_seo_brief

def generate_brief_section():
    st.header("Phase 1: Generate Initial SEO Brief")
    keyword = st.text_input("Keyword (in French):")
    client_priority = st.text_input("Client's Key Business Priority:")

    if st.button("Generate SEO Brief"):
        anthropic_api_key = st.session_state.get("chatbot_api_key")
        serpapi_api_key = st.session_state.get("serpapi_key")
        model = st.session_state.get("model")
        temperature = st.session_state.get("temperature")
        max_tokens = st.session_state.get("max_tokens")

        if not anthropic_api_key:
            st.info("Please add your Anthropic API key to continue.")
            st.stop()
        if not serpapi_api_key:
            st.info("Please add your SerpAPI key to continue.")
            st.stop()

        urls = get_google_search_results(keyword, serpapi_api_key)
        
        if not urls:
            st.info("No sources found. Please check your API key or keyword.")
            st.stop()

        sources = [scrape_text_from_url(url) for url in urls]

        seo_title, seo_meta, brief = generate_seo_brief(
            keyword, sources, client_priority, model, temperature, max_tokens, anthropic_api_key
        )

        st.session_state["generated_brief"] = f"<seotitle>{seo_title}</seotitle>\n<seometa>{seo_meta}</seometa>\n<brief>{brief}</brief>"

    if st.session_state["generated_brief"]:
        st.subheader("Generated SEO Brief")
        st.markdown(st.session_state["generated_brief"])
