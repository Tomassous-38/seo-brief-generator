from langchain_anthropic import ChatAnthropic

def generate_seo_brief(keyword, sources, client_priority, model, temperature, max_tokens, api_key):
    llm = ChatAnthropic(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key
    )

    prompt = f"""
    You will act as an SEO content specialist to create a comprehensive, SEO-optimized brief for a writer who will be tasked with writing an article on the keyword I provide. The keyword will be in French, and the brief will be in French. 

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

    messages = [
        {"role": "user", "content": prompt}
    ]

    response = llm.invoke(messages)

    brief_start = response.content.find("<brief>") + len("<brief>")
    brief_end = response.content.find("</brief>")
    brief = response.content[brief_start:brief_end].strip()

    seo_title_start = response.content.find("<seotitle>") + len("<seotitle>")
    seo_title_end = response.content.find("</seotitle>")
    seo_title = response.content[seo_title_start:seo_title_end].strip()

    seo_meta_start = response.content.find("<seometa>") + len("<seometa>")
    seo_meta_end = response.content.find("</seometa>")
    seo_meta = response.content[seo_meta_start:seo_meta_end].strip()

    return seo_title, seo_meta, brief

def improve_brief(current_brief, feedback, model, temperature, max_tokens, api_key):
    llm = ChatAnthropic(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key
    )

    improvement_prompt = f"""
    The following is an SEO brief that was generated for an article:
    {current_brief}

    The user has provided the following feedback to improve the brief:
    {feedback}

    Please provide an updated version of the SEO brief incorporating the feedback. Ensure the updated brief is inside <brief> tags and formatted in markdown.
    """

    messages = [
        {"role": "user", "content": improvement_prompt}
    ]

    response = llm.invoke(messages)

    brief_start = response.content.find("<brief>") + len("<brief>")
    brief_end = response.content.find("</brief>")
    improved_brief = response.content[brief_start:brief_end].strip()

    return improved_brief
