from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from story_generator import generate_complete_story

app = FastAPI(title="AI Story Writer")

GENRES = ["Fantasy", "Mystery", "Sci-Fi", "Adventure", "Horror"]
LENGTHS = ["Short", "Medium", "Long"]

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AI Story Writer</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #fffdf8;
      color: #2c2c2c;
      min-height: 100vh;
    }
    .container { max-width: 820px; margin: 0 auto; padding: 2rem 1.25rem 3rem; }
    .hero {
      background: #f6f1e8;
      border-radius: 20px;
      padding: 2rem;
      text-align: center;
      margin-bottom: 2rem;
    }
    .hero h1 { font-size: 2rem; margin-bottom: 0.5rem; }
    .hero p { color: #666; line-height: 1.6; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem; }
    @media (max-width: 600px) { .grid { grid-template-columns: 1fr; } }
    label { display: block; font-weight: 600; margin-bottom: 0.4rem; font-size: 0.95rem; }
    select, textarea {
      width: 100%;
      border: 1px solid #e5e7eb;
      border-radius: 12px;
      padding: 0.75rem 1rem;
      font-size: 1rem;
      background: #fff;
    }
    textarea { min-height: 160px; resize: vertical; margin-bottom: 1rem; font-family: inherit; }
    button {
      width: 100%;
      background: #7c3aed;
      color: #fff;
      border: none;
      border-radius: 12px;
      padding: 1rem;
      font-size: 1.1rem;
      font-weight: 600;
      cursor: pointer;
    }
    button:hover { background: #6d28d9; }
    button:disabled { opacity: 0.7; cursor: not-allowed; }
    .story-card {
      background: #fff;
      border: 1px solid #e5e7eb;
      border-radius: 15px;
      padding: 1.5rem;
      margin-top: 1.5rem;
      white-space: pre-wrap;
      line-height: 1.7;
    }
    .error {
      background: #fef2f2;
      color: #b91c1c;
      border: 1px solid #fecaca;
      border-radius: 12px;
      padding: 1rem;
      margin-top: 1rem;
    }
    .hidden { display: none; }
    .actions { margin-top: 1rem; }
    .actions a {
      display: inline-block;
      padding: 0.6rem 1rem;
      background: #f6f1e8;
      border-radius: 10px;
      color: #2c2c2c;
      text-decoration: none;
      font-weight: 500;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="hero">
      <h1>📖 AI Story Writer</h1>
      <p>Turn a simple idea into a complete story with title, characters, and narrative.</p>
    </div>

    <form id="story-form">
      <div class="grid">
        <div>
          <label for="genre">📚 Genre</label>
          <select id="genre" name="genre">
            <option>Fantasy</option>
            <option>Mystery</option>
            <option>Sci-Fi</option>
            <option>Adventure</option>
            <option>Horror</option>
          </select>
        </div>
        <div>
          <label for="length">📏 Story Length</label>
          <select id="length" name="length">
            <option>Short</option>
            <option selected>Medium</option>
            <option>Long</option>
          </select>
        </div>
      </div>

      <label for="idea">✨ Story Idea</label>
      <textarea id="idea" name="idea" placeholder="Example: A dragon discovers a hidden city in the clouds..." required></textarea>

      <button type="submit" id="submit-btn">✨ Generate Story</button>
    </form>

    <div id="error" class="error hidden"></div>
    <div id="result" class="story-card hidden"></div>
    <div id="actions" class="actions hidden">
      <a id="download-link" href="#" download="story.txt">⬇ Download Story</a>
    </div>
  </div>

  <script>
    const form = document.getElementById("story-form");
    const submitBtn = document.getElementById("submit-btn");
    const errorEl = document.getElementById("error");
    const resultEl = document.getElementById("result");
    const actionsEl = document.getElementById("actions");
    const downloadLink = document.getElementById("download-link");

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      errorEl.classList.add("hidden");
      resultEl.classList.add("hidden");
      actionsEl.classList.add("hidden");
      submitBtn.disabled = true;
      submitBtn.textContent = "Creating your story...";

      try {
        const response = await fetch("/api/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            idea: document.getElementById("idea").value,
            genre: document.getElementById("genre").value,
            length: document.getElementById("length").value,
          }),
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail || "Failed to generate story.");
        }

        resultEl.textContent = data.story;
        resultEl.classList.remove("hidden");

        const blob = new Blob([data.story], { type: "text/plain" });
        downloadLink.href = URL.createObjectURL(blob);
        actionsEl.classList.remove("hidden");
      } catch (err) {
        errorEl.textContent = err.message;
        errorEl.classList.remove("hidden");
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "✨ Generate Story";
      }
    });
  </script>
</body>
</html>
"""


class StoryRequest(BaseModel):
    idea: str = Field(min_length=1)
    genre: str = "Fantasy"
    length: str = "Medium"


@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE


@app.post("/api/generate")
def generate_story(request: StoryRequest):
    if request.genre not in GENRES:
        raise HTTPException(status_code=400, detail="Invalid genre.")
    if request.length not in LENGTHS:
        raise HTTPException(status_code=400, detail="Invalid length.")

    try:
        story = generate_complete_story(
            request.idea.strip(),
            request.genre,
            request.length,
        )
        return {"story": story}
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Story generation failed. Check your API key or try again later.",
        )
