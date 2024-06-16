import streamlit as st
from utils.chat_utils import improve_brief

def improve_brief_section():
    st.header("Phase 2: Improve the SEO Brief")

    for msg in st.session_state["improvement_messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    if improvement_prompt := st.chat_input("Provide feedback to improve the brief:"):
        anthropic_api_key = st.session_state.get("chatbot_api_key")
        model = st.session_state.get("model")
        temperature = st.session_state.get("temperature")
        max_tokens = st.session_state.get("max_tokens")

        if not anthropic_api_key:
            st.info("Please add your Anthropic API key to continue.")
            st.stop()

        st.session_state["improvement_messages"].append({"role": "user", "content": improvement_prompt})
        st.chat_message("user").write(improvement_prompt)

        improved_brief = improve_brief(
            st.session_state["generated_brief"], improvement_prompt, model, temperature, max_tokens, anthropic_api_key
        )

        st.session_state["improvement_messages"].append({"role": "assistant", "content": improved_brief})
        st.chat_message("assistant").write(improved_brief)
