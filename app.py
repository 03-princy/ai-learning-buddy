import json
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

# Session state used to keep the quiz (and the student's answers) alive
# across reruns, since Streamlit reruns the whole script on every click.
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = None
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False


def generate_quiz(topic: str):
    """Ask Gemini for 5 MCQs as structured JSON so the UI can render
    clickable options and grade them, instead of just printing text."""
    prompt = (
        f"Create exactly 5 multiple-choice questions on the topic '{topic}' "
        "for a beginner. For each question provide 4 answer options."
    )
    schema = {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
                        "options": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "correct_index": {
                            "type": "integer",
                            "description": "0-based index of the correct option",
                        },
                        "explanation": {"type": "string"},
                    },
                    "required": [
                        "question",
                        "options",
                        "correct_index",
                        "explanation",
                    ],
                },
            }
        },
        "required": ["questions"],
    }

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
        ),
    )
    data = json.loads(response.text)
    return data["questions"]


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
    elif option == "Generate Quiz":
        # Reset any previous quiz/answers, then fetch a fresh one.
        st.session_state.quiz_submitted = False
        st.session_state.quiz_questions = None
        with st.spinner("Building your quiz..."):
            try:
                st.session_state.quiz_questions = generate_quiz(topic)
            except Exception as e:
                st.error(f"Something went wrong calling Gemini: {e}")
    else:
        if option == "Explain Concept":
            prompt = f"Explain {topic} in simple language for a beginner."
        elif option == "Real-Life Example":
            prompt = f"Give one simple real-life example of {topic}."
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

# ─────────────────────────────────────────────────────────
# Interactive Quiz Renderer
# ─────────────────────────────────────────────────────────
if st.session_state.quiz_questions:
    st.divider()
    st.subheader("📝 Your Quiz")

    questions = st.session_state.quiz_questions
    user_answers = {}

    with st.form("quiz_form"):
        for i, q in enumerate(questions):
            st.markdown(f"**Question {i + 1}. {q['question']}**")
            user_answers[i] = st.radio(
                label="Choose one:",
                options=list(range(len(q["options"]))),
                format_func=lambda idx, q=q: q["options"][idx],
                key=f"q_{i}",
                index=None,
                label_visibility="collapsed",
            )
            st.write("")  # small spacer between questions

        submitted = st.form_submit_button("Submit Quiz")

    if submitted:
        st.session_state.quiz_submitted = True

    if st.session_state.quiz_submitted:
        score = 0
        st.divider()
        st.subheader("✅ Results")

        for i, q in enumerate(questions):
            chosen = user_answers.get(i)
            correct = q["correct_index"]
            is_correct = chosen == correct

            if chosen is None:
                st.warning(f"Question {i + 1}: You didn't select an answer.")
            elif is_correct:
                score += 1
                st.success(f"Question {i + 1}: Correct! ✅")
            else:
                st.error(
                    f"Question {i + 1}: Incorrect ❌ — you chose "
                    f"\"{q['options'][chosen]}\", the correct answer is "
                    f"\"{q['options'][correct]}\"."
                )
            st.caption(f"💡 {q['explanation']}")

        st.markdown(f"### Score: {score} / {len(questions)}")

        if st.button("🔄 Try a New Quiz"):
            st.session_state.quiz_questions = None
            st.session_state.quiz_submitted = False
            st.rerun()