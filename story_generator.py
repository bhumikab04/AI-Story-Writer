from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

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

    return llm.invoke(prompt).content