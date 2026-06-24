# AI Story Writer & Narrator

A Streamlit app that turns a short story idea into a complete tale using **Google Gemini**, with optional **text-to-speech narration** powered by gTTS.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.58+-red.svg)

## Features

- **Story generation** — Enter an idea, pick a genre and length, and get a structured story with title, characters, and full narrative
- **Audio narration** — Listen to your story with built-in text-to-speech
- **Download** — Save the generated story as a `.txt` file
- **Story history** — Browse previously generated ideas in the sidebar
- **Polished UI** — Clean, book-inspired layout with a warm color palette

## Tech Stack

| Layer | Tools |
|-------|-------|
| Frontend | Streamlit |
| LLM | Google Gemini (`gemini-2.5-flash`) via LangChain |
| TTS | gTTS |
| Config | python-dotenv |

## Project Structure

```
AI-Story-Writer/
├── app.py              # FastAPI app for Vercel deployment
├── streamlit_app.py    # Streamlit UI for local development
├── story_generator.py  # Gemini story generation
├── tts.py              # Text-to-speech helper
├── prompts.py          # Prompt templates
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── .streamlit/
    └── config.toml     # Streamlit theme config
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/bhumikab04/AI-Story-Writer.git
cd AI-Story-Writer
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

### 3. Configure your API key

```bash
cp .env.example .env
```

Open `.env` and add your Google API key:

```
GOOGLE_API_KEY=your_google_api_key_here
```

Get a key from [Google AI Studio](https://aistudio.google.com/apikey).

### 4. Run the app locally

**Streamlit UI (with audio narration):**

```bash
streamlit run streamlit_app.py
```

**FastAPI UI (same as Vercel deployment):**

```bash
uvicorn app:app --reload
```

The Streamlit app opens at `http://localhost:8501`. The FastAPI app opens at `http://localhost:8000`.

## Deploy on Vercel

This project includes a FastAPI entrypoint (`app.py`) for Vercel serverless deployment.

1. Import the repo on [Vercel](https://vercel.com)
2. Add `GOOGLE_API_KEY` in **Project Settings → Environment Variables**
3. Redeploy — Vercel uses `app.py` via the FastAPI preset (`pyproject.toml` entrypoint)

> **Note:** Streamlit cannot run on Vercel. Use `streamlit_app.py` locally for the full Streamlit experience with TTS narration.

## Usage

1. Choose a **genre** (Fantasy, Mystery, Sci-Fi, Adventure, or Horror)
2. Select a **story length** (Short, Medium, or Long)
3. Enter your **story idea** in the text area
4. Click **Generate Story**
5. Read the result, listen to the audio narration, or download the story

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GOOGLE_API_KEY` | Your Google Gemini API key (required on Vercel and locally) |
| `GEMINI_API_KEY` | Alternative env var name also supported |

## License

MIT
