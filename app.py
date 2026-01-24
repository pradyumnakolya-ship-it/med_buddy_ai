import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
from model import predict_disease

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Medi Buddy", page_icon="🩺", layout="wide")

# ---------------- DATA STORAGE ----------------
FILE = "patient_history.csv"

if not os.path.exists(FILE):
    pd.DataFrame(
        columns=["Date", "Symptoms", "Prediction"]
    ).to_csv(FILE, index=False)

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
menu = st.sidebar.radio(
    "Menu",
    [
        "Home",
        "Symptom Checker",
        "ML Disease Prediction",
        "Disease Info",
        "Medicine Info",
        "Patient History",
        "Analytics",
        "Emergency",
        "About",
    ],
)

# ---------------- UI ----------------
st.title("🩺 Medi Buddy")
st.warning("⚠️ Educational use only. Not a medical diagnosis system.")

# ---------------- HOME ----------------
if menu == "Home":
    st.write(
        """
        **Medi Buddy** is an AI-powered medical awareness assistant.
        
        This cloud version supports:
        - Text-based symptom analysis
        - Rule-based suggestions
        - ML-based disease prediction
        - Patient history tracking
        - Analytics dashboard
        """
    )

# ---------------- SYMPTOM CHECKER ----------------
elif menu == "Symptom Checker":
    symptoms = st.text_area("Enter your symptoms")

    if st.button("Analyze"):
        result = rule_based(symptoms)
        save_history(symptoms, result)
        st.success(result)

# ---------------- ML PREDICTION ----------------
elif menu == "ML Disease Prediction":
    st.subheader("AI Disease Prediction")

    fever = st.checkbox("Fever")
    cough = st.checkbox("Cough")
    headache = st.checkbox("Headache")
    fatigue = st.checkbox("Fatigue")

    if st.button("Predict"):
        features = [fever, cough, headache, fatigue]
        prediction = predict_disease(features)
        save_history(str(features), prediction)
        st.success(f"Predicted Disease: **{prediction}**")

# ---------------- INFO ----------------
elif menu == "Disease Info":
    st.info("Supported diseases: Flu, Migraine, Viral Infection")

elif menu == "Medicine Info":
    st.info("Common medicines: Paracetamol, Ibuprofen")

# ---------------- HISTORY ----------------
elif menu == "Patient History":
    df = pd.read_csv(FILE)
    st.dataframe(df, use_container_width=True)

# ---------------- ANALYTICS ----------------
elif menu == "Analytics":
    df = pd.read_csv(FILE)
    if not df.empty:
        fig, ax = plt.subplots()
        df["Prediction"].value_counts().plot(kind="bar", ax=ax)
        ax.set_xlabel("Disease")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    else:
        st.info("No data available for analytics.")

# ---------------- EMERGENCY ----------------
elif menu == "Emergency":
    st.error("🚨 Please contact emergency medical services immediately!")

# ---------------- ABOUT ----------------
elif menu == "About":
    st.write(
        """
        **Medi Buddy**
        
        An AI-inspired medical awareness system built using Streamlit.
        
        Features:
        - Rule-based symptom analysis
        - Machine learning disease prediction
        - Patient history storage
        - Analytics visualization
        
        © 2026 Academic Project
        """
    )



