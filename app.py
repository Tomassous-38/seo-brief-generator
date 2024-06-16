import streamlit as st
from langchain_anthropic import ChatAnthropic

# Title and description
st.title("💬 SEO Brief Generator")
st.caption("🚀 A Streamlit chatbot powered by Anthropic Claude")

# Sidebar for API key input and configuration
with st.sidebar:
    anthropic_api_key = st.text_input("Anthropic API Key", key="chatbot_api_key", type="password")
    
    model = st.selectbox(
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
    temperature = st.slider("Select Temperature", 0.0, 1.0, 0.0, 0.1)
    max_tokens = st.number_input("Max Tokens", min_value=1, max_value=4000, value=1024)

# Initialize session state
if "generated_brief" not in st.session_state:
    st.session_state["generated_brief"] = ""
if "improvement_messages" not in st.session_state:
    st.session_state["improvement_messages"] = []

# Phase 1: Initial Brief Generation
st.header("Phase 1: Generate Initial SEO Brief")
keyword = st.text_input("Keyword (in French):")
source1 = st.text_area("Source 1:")
source2 = st.text_area("Source 2:")
source3 = st.text_area("Source 3:")
source4 = st.text_area("Source 4:")
source5 = st.text_area("Source 5:")
source6 = st.text_area("Source 6:")
source7 = st.text_area("Source 7:")
source8 = st.text_area("Source 8:")
client_priority = st.text_input("Client's Key Business Priority:")

if st.button("Generate SEO Brief"):
    if not anthropic_api_key:
        st.info("Please add your Anthropic API key to continue.")
        st.stop()

    # Function to generate SEO brief
    def generate_seo_brief(keyword, sources, client_priority, model, temperature, max_tokens):
        # Initialize Langchain with the Claude model from Anthropic
        llm = ChatAnthropic(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
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
        <source1>
        {sources[0]}
        </source1>
        <source2>
        {sources[1]}
        </source2>
        <source3>
        {sources[2]}
        </source3>
        <source4>
        {sources[3]}
        </source4>
        <source5>
        {sources[4]}
        </source5>
        <source6>
        {sources[5]}
        </source6>
        <source7>
        {sources[6]}
        </source7>
        <source8>
        {sources[7]}
        </source8>

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

        Provide your finished brief inside <brief> tags. Remember, the goal is to create an in-depth, well-structured outline that will guide the writer in creating a comprehensive, SEO-optimized article on the given keyword. Do not make any comments, just display the SEO Metas into <seotitle> <seometa> and the brief in <brief>
        """

        # Prepare the messages for the API
        messages = [
            {"role": "user", "content": prompt}
        ]

        # Call the API and get the response
        response = llm.invoke(messages)

        # Extract the brief from the response
        brief_start = response.content.find("<brief>") + len("<brief>")
        brief_end = response.content.find("</brief>")
        brief = response.content[brief_start:brief_end].strip()

        # Extract the SEO metas from the response
        seo_title_start = response.content.find("<seotitle>") + len("<seotitle>")
        seo_title_end = response.content.find("</seotitle>")
        seo_title = response.content[seo_title_start:seo_title_end].strip()

        seo_meta_start = response.content.find("<seometa>") + len("<seometa>")
        seo_meta_end = response.content.find("</seometa>")
        seo_meta = response.content[seo_meta_start:seo_meta_end].strip()

        return seo_title, seo_meta, brief

    # Generate the SEO brief
    sources = [source1, source2, source3, source4, source5, source6, source7, source8]
    seo_title, seo_meta, brief = generate_seo_brief(keyword, sources, client_priority, model, temperature, max_tokens)
    
    # Store the generated brief in session state
    st.session_state["generated_brief"] = f"<seotitle>{seo_title}</seotitle>\n<seometa>{seo_meta}</seometa>\n<brief>{brief}</brief>"

# Display the generated brief
if st.session_state["generated_brief"]:
    st.subheader("Generated SEO Brief")
    st.markdown(st.session_state["generated_brief"])

# Phase 2: Interactive Improvement
st.header("Phase 2: Improve the SEO Brief")

# Display chat messages from session state
for msg in st.session_state["improvement_messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input functionality for improvements
if improvement_prompt := st.chat_input("Provide feedback to improve the brief:"):
    if not anthropic_api_key:
        st.info("Please add your Anthropic API key to continue.")
        st.stop()

    # Append user message to session state
    st.session_state["improvement_messages"].append({"role": "user", "content": improvement_prompt})
    st.chat_message("user").write(improvement_prompt)

    # Function to get improvement suggestions
    def improve_brief(current_brief, feedback, model, temperature, max_tokens):
        # Initialize Langchain with the Claude model from Anthropic
        llm = ChatAnthropic(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=anthropic_api_key
        )

        # Formulate the improvement request for the Claude API
        improvement_prompt = f"""
        The following is an SEO brief that was generated for an article:
        {current_brief}

        The user has provided the following feedback to improve the brief:
        {feedback}

        Please provide an updated version of the SEO brief incorporating the feedback. Ensure the updated brief is inside <brief> tags.
        """

        # Prepare the messages for the API
        messages = [
            {"role": "user", "content": improvement_prompt}
        ]

        # Call the API and get the response
        response = llm.invoke(messages)

        # Extract the improved brief from the response
        brief_start = response.content.find("<brief>") + len("<brief>")
        brief_end = response.content.find("</brief>")
        improved_brief = response.content[brief_start:brief_end].strip()

        return improved_brief

    # Get the improved brief
    improved_brief = improve_brief(st.session_state["generated_brief"], improvement_prompt, model, temperature, max_tokens)

    # Append the assistant's response to session state
    st.session_state["improvement_messages"].append({"role": "assistant", "content": improved_brief})
    st.chat_message("assistant").write(improved_brief)
