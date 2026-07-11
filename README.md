# 🎓 AI Learning Buddy

A small AI-powered web app: type any topic, pick an activity (explanation, real-life example, interactive quiz, or ask-anything), and Gemini generates the answer instantly in your browser.

Built with **Streamlit** (UI) and the **Gemini API** (generation), run locally with a Python virtual environment.

## Files

| File | Purpose |
|---|---|
| `app.py` | The Streamlit application |
| `requirements.txt` | Python dependencies |
| `.env.example` | Template showing which environment variable to set (copy to `.env` and fill in your real key) |
| `.gitignore` | Keeps `.env`, `venv/`, and other local-only files out of git |

## Setup

**1. Clone the repo and enter the folder:**
```bash
git clone https://github.com/03-princy/ai-learning-buddy.git
cd ai-learning-buddy
```

**2. Create and activate a virtual environment:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```
Requires **Python 3.9+** (the Gemini SDK doesn't support older versions).

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Add your Gemini API key.**
Copy `.env.example` to `.env`:
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```
Then open `.env` and paste in your own key (get one free at https://aistudio.google.com/app/apikey):
```
GEMINI_API_KEY=your_real_key_here
```

⚠️ **Never commit `.env` or share it.** It's already excluded via `.gitignore`. If a key is ever exposed (pasted in chat, screenshot, public repo, etc.), regenerate it immediately at the link above.

**5. Run the app:**
```bash
streamlit run app.py
```
Streamlit opens the app in your browser automatically at `http://localhost:8501`.

## How the app works

- You type a **topic** and choose an **activity** from the dropdown.
- **Explain Concept / Real-Life Example / Ask Anything** — Gemini generates a plain-text response, displayed directly on the page.
- **Generate Quiz** — Gemini returns 5 multiple-choice questions as structured JSON (question, 4 options, correct answer, explanation). The app renders them as clickable radio-button questions in a form; clicking **Submit Quiz** grades every answer, shows ✅/❌ with the correct answer and explanation for each, and a final score. A **Try a New Quiz** button resets it for another round.
- Requests are sent to the `gemini-3.5-flash` model via the current `google-genai` SDK.

## Troubleshooting

- **`ModuleNotFoundError`** — make sure your venv is activated and you've run `pip install -r requirements.txt`.
- **`ImportError: cannot import name 'genai' from 'google'`** — usually a leftover install of the old, deprecated `google-generativeai` package conflicting with the new `google-genai`. Fix with:
  ```bash
  pip uninstall -y google-generativeai google-ai-generativelanguage
  pip install --force-reinstall --no-deps google-genai
  ```
- **404 "model no longer available"** — Google retires Gemini model versions periodically. Check https://ai.google.dev/gemini-api/docs/models for the current model name and update `MODEL_NAME` in `app.py`.
- **"No Gemini API key found"** — confirm `.env` exists in the project root (not inside `venv/`) and contains a valid `GEMINI_API_KEY`.
- **"Address already in use"** — another Streamlit process is already running on port 8501. Stop it (`Ctrl+C` in its terminal) before starting a new one.
- **Nothing happens on Generate** — make sure the Topic box isn't empty.
