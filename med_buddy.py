import streamlit as st
import pandas as pd
import numpy as np
import speech_recognition as sr
import pyttsx3
import matplotlib.pyplot as plt
from datetime import datetime
from model import predict_disease

# ---------------- CONFIG ----------------
st.set_page_config("Medi Buddy", "🩺", layout="wide")

# ---------------- VOICE ----------------
engine = pyttsx3.init()
engine.setProperty("rate", 160)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except:
        return ""

# ---------------- DATA STORAGE ----------------
FILE = "patient_history.csv"

if not os.path.exists(FILE):
    pd.DataFrame(columns=["Date", "Symptoms", "Prediction"]).to_csv(FILE, index=False)

def save_history(symptoms, result):
    df = pd.read_csv(FILE)
    df.loc[len(df)] = [datetime.now(), symptoms, result]
    df.to_csv(FILE, index=False)

# ---------------- RULE BASED ----------------
def rule_based(symptoms):
    s = symptoms.lower()
    if "fever" in s and "cough" in s:
        return "Possible Flu or Viral Infection"
    if "headache" in s:
        return "Possible Migraine or Stress"
    return "Condition unclear"

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio("Menu", [
    "Home",
    "Symptom Checker",
    "ML Disease Prediction",
    "Disease Info",
    "Medicine Info",
    "Patient History",
    "Analytics",
    "Emergency",
    "About"
])

# ---------------- UI ----------------
st.title("🩺 Medi Buddy")
st.warning("Educational use only. Not a medical diagnosis system.")

# ---------------- HOME ----------------
if menu == "Home":
    st.write("Offline medical awareness assistant with AI + Voice.")

# ---------------- SYMPTOMS ----------------
elif menu == "Symptom Checker":
    text = st.text_area("Enter symptoms")
    if st.button("Analyze"):
        result = rule_based(text)
        save_history(text, result)
        st.success(result)
        speak(result)

    if st.button("🎤 Speak"):
        voice = listen()
        if voice:
            result = rule_based(voice)
            save_history(voice, result)
            st.success(result)
            speak(result)

# ---------------- ML PREDICTION ----------------
elif menu == "ML Disease Prediction":
    st.subheader("AI Prediction")
    fever = st.checkbox("Fever")
    cough = st.checkbox("Cough")
    headache = st.checkbox("Headache")
    fatigue = st.checkbox("Fatigue")

    if st.button("Predict"):
        features = [fever, cough, headache, fatigue]
        prediction = predict_disease(features)
        save_history(str(features), prediction)
        st.success(f"Predicted Disease: {prediction}")
        speak(f"Predicted disease is {prediction}")

# ---------------- INFO ----------------
elif menu == "Disease Info":
    st.info("Diabetes, Flu, Migraine supported")

elif menu == "Medicine Info":
    st.info("Paracetamol, Ibuprofen supported")

# ---------------- HISTORY ----------------
elif menu == "Patient History":
    df = pd.read_csv(FILE)
    st.dataframe(df)

# ---------------- ANALYTICS ----------------
elif menu == "Analytics":
    df = pd.read_csv(FILE)
    if not df.empty:
        df["Prediction"].value_counts().plot(kind="bar")
        st.pyplot(plt)

# ---------------- EMERGENCY ----------------
elif menu == "Emergency":
    st.error("🚨 Call emergency services immediately!")
    speak("Please seek emergency medical help.")

# ---------------- ABOUT ----------------
elif menu == "About":
    st.write("""
    Medi Buddy is an offline AI-inspired medical assistant.
    Includes rule-based logic, ML prediction, voice interaction,
    analytics, and data storage.

    © 2026 Academic Project
    """)
    
