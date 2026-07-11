import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ─────────────────────────────────────────────────────────
# Configure Gemini API
# ─────────────────────────────────────────────────────────
# Best practice: read the key from an environment variable so it never
# ends up hard-coded in a file you might share or upload.
# load_dotenv() reads a local .env file (if present) into the environment.
# In Colab, set it with:  os.environ["GEMINI_API_KEY"] = "your_key_here"
# (in a cell ABOVE the %%writefile cell, before you run the app)
load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-3.5-flash"

# ─────────────────────────────────────────────────────────
# Page and Layout
# ─────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Learning Buddy", page_icon="🎓")
st.title("🎓 AI Learning Buddy")
st.caption("Type a topic, pick an activity, and let Gemini teach you.")

topic = st.text_input("Enter a Topic")
option = st.selectbox(
    "Choose Activity",
    [
        "Explain Concept",
        "Real-Life Example",
        "Generate Quiz",
        "Ask Anything",
    ],
)

# ─────────────────────────────────────────────────────────
# App Logic
# ─────────────────────────────────────────────────────────
if st.button("Generate"):
    if topic == "":
        st.warning("Please enter a topic.")
    elif API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        st.error(
            "No Gemini API key found. Set the GEMINI_API_KEY environment "
            "variable (or edit API_KEY in app.py) before running the app."
        )
    else:
        if option == "Explain Concept":
            prompt = f"Explain {topic} in simple language for a beginner."
        elif option == "Real-Life Example":
            prompt = f"Give one simple real-life example of {topic}."
        elif option == "Generate Quiz":
            prompt = f"Create 5 MCQs on {topic} with answers."
        else:
            prompt = topic

        with st.spinner("Thinking..."):
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt,
                )
                st.write(response.text)
            except Exception as e:
                st.error(f"Something went wrong calling Gemini: {e}")