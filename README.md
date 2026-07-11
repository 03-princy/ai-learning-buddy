# 🎓 AI Learning Buddy

A small AI-powered web app: type any topic, pick an activity (explanation, real-life example, quiz, or ask-anything), and Gemini generates the answer instantly in your browser.

Built with **Streamlit** (UI), **Google Colab** (runtime), **Gemini API** (generation), and **ngrok** (public link).

## Files

| File | Purpose |
|---|---|
| `app.py` | The Streamlit application |
| `requirements.txt` | Python dependencies |
| `AI_Learning_Buddy_Colab.ipynb` | Ready-to-run Colab notebook that installs everything, starts the app, and exposes it with ngrok |

## Quickest way to run it: Google Colab

1. Upload `AI_Learning_Buddy_Colab.ipynb` to https://colab.research.google.com (File → Upload notebook).
2. Also upload `app.py` into the Colab file browser (left sidebar), **or** just run the notebook's `%%writefile app.py` cell, which creates it for you.
3. In the "Set Your Keys" cell, paste your own:
   - Gemini API key — get one free at https://aistudio.google.com/app/apikey
   - ngrok auth token — get one free at https://ngrok.com
4. Run every cell top to bottom (Runtime → Run all).
5. Click the public URL printed by the ngrok cell to open your live app.

⚠️ **Never share a notebook with your real keys pasted in.** The notebook stores your key in an environment variable (not hard-coded in `app.py`), so `app.py` itself is always safe to share — just don't share the notebook after you've typed your keys into it, or regenerate the keys afterward.

## Running it locally instead (optional)

If you'd rather run it on your own machine instead of Colab:

```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your_key_here"      # macOS/Linux
# set GEMINI_API_KEY=your_key_here          # Windows (cmd)
streamlit run app.py
```

Streamlit will open the app directly in your browser at `http://localhost:8501` — no ngrok needed since it's already on your machine.

## How the app works

- You type a **topic** and choose an **activity** from the dropdown.
- Clicking **Generate** builds a prompt based on your choice (e.g. "Explain photosynthesis in simple language for a beginner") and sends it to the `gemini-2.5-flash` model.
- The model's response is displayed on the page with `st.write()`.

## Troubleshooting

- **"Address already in use"** — another Streamlit process is already running on that port. Restart the Colab runtime and rerun cells in order.
- **ngrok link shows an error page** — the app may not have finished starting; wait a few seconds and refresh, or check `nohup.out`.
- **"Invalid API key"** — double-check the key has no extra spaces and was set correctly.
- **Nothing happens on Generate** — make sure the Topic box isn't empty.
- **Colab session disconnected** — the free tier disconnects after inactivity; rerun all cells from the top.
