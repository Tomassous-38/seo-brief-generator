import streamlit as st
from langchain_anthropic import ChatAnthropic
import os

# Title and description
st.title("💬 SEO Brief Generator")
st.caption("🚀 A Streamlit chatbot powered by Anthropic Claude")

# Sidebar for API key input
with st.sidebar:
    anthropic_api_key = st.text_input("Anthropic API Key", key="chatbot_api_key", type="password")
    st.write("[Get an Anthropic API key](https://www.anthropic.com/)")
    st.write("[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)")
    st.write("[![Open in GitHub Codespaces](https://codespaces.badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you with your SEO brief today?"}]

# Display chat messages from session state
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Function to generate SEO brief
def generate_seo_brief(keyword, sources, client_priority):
    # Initialize Langchain with the Claude model from Anthropic
    llm = ChatAnthropic(
        model="claude-3-sonnet-20240229",
        temperature=0,
        max_tokens=1024,
        api_key=anthropic_api_key
    )

    # Formulate the request for the Claude API
    prompt = f"""
    You will act as an SEO content specialist to create a comprehensive, SEO-optimized brief for a writer who will be tasked with writing an article on the keyword I provide. The Keyword will be in French, and the brief will be in French. 

    Here is the target keyword to optimize the article brief for:
    <keyword>
    {keyword}
    </keyword>

    Structure the brief in markdown format, using <hn> tags to outline the sections and subsections the article should include. Under each <hn> heading, provide detailed bullet points covering the specific elements, information, and topics that section of the article should discuss.

    To help with researching and gathering relevant information for the brief, I will provide some sources, which may include academic articles or other pertinent articles:
    <sources>
    {sources}
    </sources>

    Be very thorough and detailed in fleshing out the brief. I may provide additional remarks or suggestions to help improve and refine the brief.

    In addition to the content outline, please suggest the following SEO meta elements:
    - <title>
    - Meta description 
    - <h1>

    These meta elements should all include the target keyword, adhere to Google's recommended lengths, accurately reflect the article's content, and have an informative tone suitable for a long-form educational article.

    Here is the client's key business priority that should be tied into the article where most relevant and natural:
    <client_priority>
    {client_priority}
    </client_priority>

    Provide your finished brief inside <brief> tags. Remember, the goal is to create an in-depth, well-structured outline that will guide the writer in creating a comprehensive, SEO-optimized article on the given keyword.
    """

    # Prepare the messages for the API
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    # Call the API and get the response
    response = llm.invoke(messages)

    # Extract the brief from the response
    brief_start = response.content.find("<brief>") + len("<brief>")
    brief_end = response.content.find("</brief>")
    brief = response.content[brief_start:brief_end].strip()

    return brief

# Chat input functionality
if prompt := st.chat_input():
    if not anthropic_api_key:
        st.info("Please add your Anthropic API key to continue.")
        st.stop()

    # Append user message to session state
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Generate the SEO brief
    brief = generate_seo_brief(prompt, "", "")
    st.session_state["messages"].append({"role": "assistant", "content": brief})
    st.chat_message("assistant").write(brief)
