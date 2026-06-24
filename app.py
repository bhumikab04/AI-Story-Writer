import streamlit as st
from tts import create_audio
from story_generator import generate_complete_story

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Story Writer",
    page_icon="📖",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

/* Main Layout */
.main {
    padding-top: 1rem;
}

/* Generate Button */
.stButton > button {
    width: 100%;
    background-color: #7C3AED;
    color: white;
    border-radius: 12px;
    height: 55px;
    font-size: 18px;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    background-color: #6D28D9;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #F6F1E8;
}

/* Text Area */
textarea {
    border-radius: 12px !important;
}

/* Story Card */
.story-card {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #E5E7EB;
    margin-top: 20px;
}

.hero-box {
    background-color: #F6F1E8;
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION HISTORY ----------------

if "story_history" not in st.session_state:
    st.session_state.story_history = []

# ---------------- HERO SECTION ----------------

st.markdown("""
<div class="hero-box">

# 📖 AI Story Writer & Narrator

### Create beautiful AI-generated stories with narration

Turn a simple idea into a complete story, characters, and audio experience.

</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------- SIDEBAR ----------------

st.sidebar.markdown("""
# 📚 Story History

Previously generated stories
""")

for item in st.session_state.story_history:
    with st.sidebar.expander(item):
        st.write(item)

# ---------------- INPUT SECTION ----------------

col1, col2 = st.columns(2)

with col1:
    genre = st.selectbox(
        "📚 Genre",
        [
            "Fantasy",
            "Mystery",
            "Sci-Fi",
            "Adventure",
            "Horror"
        ]
    )

with col2:
    length = st.selectbox(
        "📏 Story Length",
        [
            "Short",
            "Medium",
            "Long"
        ]
    )

idea = st.text_area(
    "✨ Story Idea",
    height=180,
    placeholder="Example: A dragon discovers a hidden city in the clouds..."
)

# ---------------- GENERATE BUTTON ----------------

if st.button("✨ Generate Story"):

    if idea.strip() == "":
        st.warning("Please enter a story idea.")

    else:

        try:

            with st.spinner("Creating your story..."):

                result = generate_complete_story(
                    idea,
                    genre,
                    length
                )

                # Save history
                story_title = (
                    idea[:40] + "..."
                    if len(idea) > 40
                    else idea
                )

                st.session_state.story_history.append(
                    story_title
                )

                st.divider()

                st.subheader("📚 Generated Story")

                st.markdown(
                    f"""
                    <div class="story-card">
                    {result}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Audio Narration
                audio_file = create_audio(result)

                st.divider()

                st.subheader("🎙️ Audio Narration")

                st.audio(audio_file)

                # Download Button
                st.download_button(
                    label="⬇ Download Story",
                    data=result,
                    file_name="story.txt",
                    mime="text/plain"
                )

        except Exception:

            st.error(
                "Daily Gemini API limit reached. Please try again later or use a different API key."
            )