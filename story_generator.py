import os

from dotenv import load_dotenv

load_dotenv()

_llm = None


def _get_api_key() -> str:
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")
    return api_key


def _get_llm():
    global _llm
    if _llm is None:
        from langchain_google_genai import ChatGoogleGenerativeAI

        _llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            google_api_key=_get_api_key(),
        )
    return _llm


def generate_complete_story(idea, genre, length):
    prompt = f"""
    Create a {length} {genre} story.

    Return your response in this format:

    # TITLE

    title here

    # CHARACTERS

    main characters here

    # STORY

    full story here

    Story idea:
    {idea}
    """

    response = _get_llm().invoke(prompt)
    return response.content
