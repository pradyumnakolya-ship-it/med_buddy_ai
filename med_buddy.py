# =============================================================
# Medi Buddy: AI-Powered Voice-Enabled Medical Assistant
# =============================================================
# Author: Pradyumna K
# Description:
#   This is a comprehensive, educational medical assistant built
#   using Streamlit, OpenAI, SpeechRecognition, and pyttsx3.
#   The application supports:
#     - Text-based medical Q&A
#     - Voice commands (Speech-to-Text)
#     - Voice responses (Text-to-Speech)
#     - Symptom checker (non-diagnostic)
#     - Disease information
#     - Medicine information
#     - Emergency guidance (advisory only)
#   DISCLAIMER:
#     This application does NOT provide medical diagnosis.
#     It is intended for awareness and educational purposes only.
#     Always consult a qualified healthcare professional.
# =============================================================

# -----------------------------
# SECTION 1: IMPORTS
# -----------------------------

import streamlit as st
import openai
import speech_recognition as sr
import pyttsx3
import datetime
import json
import os
import time
import threading
from typing import List, Dict

# -----------------------------
# SECTION 2: GLOBAL CONFIG
# -----------------------------

APP_NAME = "Medi Buddy"
APP_VERSION = "1.0"

# Load OpenAI API key securely
# Expected to be stored in Streamlit secrets
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

# -----------------------------
# SECTION 3: STREAMLIT PAGE SETUP
# -----------------------------

st.set_page_config(
    page_title=f"{APP_NAME} 🩺",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🩺 Medi Buddy – Voice Enabled Medical Assistant")
st.caption("AI-powered medical awareness assistant with voice support")

# -----------------------------
# SECTION 4: DISCLAIMER
# -----------------------------

st.warning(
    "⚠️ DISCLAIMER: Medi Buddy is for educational and informational purposes only. "
    "It does NOT diagnose diseases or prescribe treatment. "
    "Always consult a qualified doctor for medical concerns."
)

# -----------------------------
# SECTION 5: UTILITY FUNCTIONS
# -----------------------------

def get_current_timestamp() -> str:
    """Return current timestamp as string."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log_interaction(user_input: str, ai_response: str) -> None:
    """Log user interactions to a local JSON file."""
    log_entry = {
        "timestamp": get_current_timestamp(),
        "user_input": user_input,
        "ai_response": ai_response
    }

    if not os.path.exists("logs.json"):
        with open("logs.json", "w") as f:
            json.dump([log_entry], f, indent=4)
    else:
        with open("logs.json", "r+") as f:
            data = json.load(f)
            data.append(log_entry)
            f.seek(0)
            json.dump(data, f, indent=4)


# -----------------------------
# SECTION 6: VOICE INPUT (SPEECH TO TEXT)
# -----------------------------

def voice_to_text(timeout: int = 5) -> str:
    """
    Capture voice input from microphone and convert to text.
    Uses Google Speech Recognition API.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Please speak clearly")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=timeout)
        except sr.WaitTimeoutError:
            return "Listening timed out."

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand your voice."
    except sr.RequestError:
        return "Speech recognition service is unavailable."


# -----------------------------
# SECTION 7: VOICE OUTPUT (TEXT TO SPEECH)
# -----------------------------

def speak_text(text: str) -> None:
    """
    Convert text to speech using pyttsx3.
    Runs in a separate thread to avoid blocking UI.
    """
    def _speak():
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.say(text)
        engine.runAndWait()

    t = threading.Thread(target=_speak)
    t.start()


# -----------------------------
# SECTION 8: OPENAI RESPONSE HANDLER
# -----------------------------

def get_ai_response(prompt: str) -> str:
    """
    Get response from OpenAI GPT model with medical safety rules.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a medical awareness assistant. "
                        "Do not diagnose diseases or prescribe medication. "
                        "Provide general information and always advise consulting a doctor."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error fetching AI response: {str(e)}"


# -----------------------------
# SECTION 9: SIDEBAR NAVIGATION
# -----------------------------

st.sidebar.title("🧭 Navigation")

menu_option = st.sidebar.radio(
    "Select a service",
    (
        "Home",
        "Symptom Checker",
        "Disease Information",
        "Medicine Information",
        "Voice Medical Assistant",
        "Emergency Guidance",
        "About"
    )
)

# -----------------------------
# SECTION 10: HOME PAGE
# -----------------------------

if menu_option == "Home":
    st.subheader("Welcome to Medi Buddy 🩺")
    st.write(
        "Medi Buddy is an AI-powered medical awareness assistant designed to help users "
        "understand common symptoms, diseases, and medicines using both text and voice."
    )

    st.markdown("""
    ### Features
    - 🩺 Symptom Checker
    - 📚 Disease Information
    - 💊 Medicine Guidance
    - 🎤 Voice Commands
    - 🗣️ Voice Assistant
    - 🚨 Emergency Awareness
    """)

# -----------------------------
# SECTION 11: SYMPTOM CHECKER
# -----------------------------

elif menu_option == "Symptom Checker":
    st.subheader("🩺 Symptom Checker")
    symptoms = st.text_area("Describe your symptoms")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Analyze Symptoms"):
            prompt = (
                f"A user reports the following symptoms: {symptoms}. "
                "Explain possible common causes and basic precautions."
            )
            response = get_ai_response(prompt)
            st.write(response)
            speak_text(response)
            log_interaction(symptoms, response)

    with col2:
        if st.button("🎤 Speak Symptoms"):
            spoken_text = voice_to_text()
            st.success(f"You said: {spoken_text}")
            response = get_ai_response(spoken_text)
            st.write(response)
            speak_text(response)
            log_interaction(spoken_text, response)

# -----------------------------
# SECTION 12: DISEASE INFORMATION
# -----------------------------

elif menu_option == "Disease Information":
    st.subheader("📚 Disease Information")
    disease_name = st.text_input("Enter disease name")

    if st.button("Get Disease Info"):
        prompt = (
            f"Explain the disease {disease_name} in simple terms, including symptoms, "
            "causes, prevention, and when to consult a doctor."
        )
        response = get_ai_response(prompt)
        st.write(response)
        speak_text(response)
        log_interaction(disease_name, response)

# -----------------------------
# SECTION 13: MEDICINE INFORMATION
# -----------------------------

elif menu_option == "Medicine Information":
    st.subheader("💊 Medicine Information")
    medicine_name = st.text_input("Enter medicine name")

    if st.button("Get Medicine Details"):
        prompt = (
            f"Provide general information about the medicine {medicine_name}, "
            "including usage, precautions, and common side effects."
        )
        response = get_ai_response(prompt)
        st.write(response)
        speak_text(response)
        log_interaction(medicine_name, response)

# -----------------------------
# SECTION 14: VOICE MEDICAL ASSISTANT
# -----------------------------

elif menu_option == "Voice Medical Assistant":
    st.subheader("🎤 Voice Medical Assistant")

    st.write("Click the button and ask your medical question using voice.")

    if st.button("🎤 Start Voice Assistant"):
        query = voice_to_text()
        st.success(f"You asked: {query}")
        response = get_ai_response(query)
        st.write(response)
        speak_text(response)
        log_interaction(query, response)

# -----------------------------
# SECTION 15: EMERGENCY GUIDANCE
# -----------------------------

elif menu_option == "Emergency Guidance":
    st.subheader("🚨 Emergency Guidance")

    st.error(
        "If this is a medical emergency, call your local emergency number immediately."
    )

    emergency_issue = st.selectbox(
        "Select an emergency situation",
        (
            "Chest pain",
            "Breathing difficulty",
            "Severe bleeding",
            "Burn injury",
            "Unconsciousness",
            "High fever"
        )
    )

    if st.button("Get Emergency Advice"):
        prompt = (
            f"Provide first-aid guidance for {emergency_issue}. "
            "Include immediate steps and advise contacting emergency services."
        )
        response = get_ai_response(prompt)
        st.write(response)
        speak_text(response)
        log_interaction(emergency_issue, response)

# -----------------------------
# SECTION 16: ABOUT PAGE
# -----------------------------

elif menu_option == "About":
    st.subheader("ℹ️ About Medi Buddy")

    st.markdown(f"""
    **Application Name:** {APP_NAME}

    **Version:** {APP_VERSION}

    **Purpose:**
    Medi Buddy is designed as an academic project demonstrating the use of AI,
    Natural Language Processing, and Voice Interfaces in healthcare awareness.

    **Technologies Used:**
    - Python
    - Streamlit
    - OpenAI GPT
    - SpeechRecognition
    - pyttsx3

    **Disclaimer:**
    This application does not replace professional medical advice.
    """)

# -----------------------------
# SECTION 17: FOOTER
# -----------------------------

st.markdown("---")
st.caption("© 2026 Medi Buddy | Educational Use Only")

# -----------------------------
# END OF FILE
# -----------------------------
