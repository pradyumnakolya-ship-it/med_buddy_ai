# =============================================================
# Medi Buddy – Streamlit Cloud Ready (Text-Based)
# =============================================================
# Author: Pradyumna K
# Purpose:
#   Cloud-deployable version of Medi Buddy with all breaking issues fixed.
#   - Works on Streamlit Cloud
#   - Uses NEW OpenAI SDK (no deprecated calls)
#   - Voice features safely DISABLED in cloud
#   - Suitable for final-year submission & viva
# =============================================================

# -----------------------------
# SECTION 1: IMPORTS
# -----------------------------

import streamlit as st
from openai import OpenAI
import datetime
import json
import os

# -----------------------------
# SECTION 2: APP CONFIG
# -----------------------------

APP_NAME = "Medi Buddy"
APP_VERSION = "1.1 (Cloud Ready)"

st.set_page_config(
    page_title="Medi Buddy 🩺",
    page_icon="🩺",
    layout="centered"
)

# -----------------------------
# SECTION 3: OPENAI CLIENT
# -----------------------------

if "OPENAI_API_KEY" not in st.secrets:
    st.error("OpenAI API key not found. Add it in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# SECTION 4: HEADER & DISCLAIMER
# -----------------------------

st.title("🩺 Medi Buddy – AI Medical Assistant")
st.caption("Cloud-deployed, text-based medical awareness assistant")

st.warning(
    "⚠️ DISCLAIMER: This application is for educational and informational purposes only. "
    "It does NOT diagnose diseases or prescribe treatment. "
    "Always consult a qualified healthcare professional."
)

# -----------------------------
# SECTION 5: UTILITY FUNCTIONS
# -----------------------------

def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log_interaction(user_input, ai_response):
    entry = {
        "time": get_timestamp(),
        "user": user_input,
        "assistant": ai_response
    }

    if not os.path.exists("logs.json"):
        with open("logs.json", "w") as f:
            json.dump([entry], f, indent=4)
    else:
        with open("logs.json", "r+") as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=4)


# -----------------------------
# SECTION 6: OPENAI RESPONSE FUNCTION
# -----------------------------

def get_ai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a medical awareness assistant. "
                        "Do not diagnose diseases or prescribe medicines. "
                        "Provide general guidance and advise consulting a doctor."
                    )
                },
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


# -----------------------------
# SECTION 7: SIDEBAR MENU
# -----------------------------

st.sidebar.title("🧭 Menu")

menu = st.sidebar.radio(
    "Choose a service",
    [
        "Home",
        "Symptom Checker",
        "Disease Information",
        "Medicine Information",
        "Emergency Guidance",
        "About"
    ]
)

# -----------------------------
# SECTION 8: HOME
# -----------------------------

if menu == "Home":
    st.subheader("Welcome to Medi Buddy")
    st.write(
        "Medi Buddy helps users understand common medical symptoms, diseases, and medicines "
        "using AI. This cloud version supports text-based interaction only."
    )

    st.markdown("""
    ### Features
    - 🩺 Symptom Checker
    - 📚 Disease Awareness
    - 💊 Medicine Information
    - 🚨 Emergency First-Aid Guidance
    - ☁️ Cloud Deployed (Streamlit)
    """)

# -----------------------------
# SECTION 9: SYMPTOM CHECKER
# -----------------------------

elif menu == "Symptom Checker":
    st.subheader("🩺 Symptom Checker")

    symptoms = st.text_area("Describe your symptoms")

    if st.button("Analyze Symptoms"):
        if symptoms.strip() == "":
            st.warning("Please enter symptoms.")
        else:
            prompt = (
                f"A user reports these symptoms: {symptoms}. "
                "Explain possible common causes and basic precautions."
            )
            response = get_ai_response(prompt)
            st.write(response)
            log_interaction(symptoms, response)

# -----------------------------
# SECTION 10: DISEASE INFORMATION
# -----------------------------

elif menu == "Disease Information":
    st.subheader("📚 Disease Information")

    disease = st.text_input("Enter disease name")

    if st.button("Get Disease Info"):
        if disease.strip() == "":
            st.warning("Please enter a disease name.")
        else:
            prompt = (
                f"Explain the disease {disease} in simple terms including symptoms, "
                "causes, prevention, and when to see a doctor."
            )
            response = get_ai_response(prompt)
            st.write(response)
            log_interaction(disease, response)

# -----------------------------
# SECTION 11: MEDICINE INFORMATION
# -----------------------------

elif menu == "Medicine Information":
    st.subheader("💊 Medicine Information")

    medicine = st.text_input("Enter medicine name")

    if st.button("Get Medicine Details"):
        if medicine.strip() == "":
            st.warning("Please enter a medicine name.")
        else:
            prompt = (
                f"Provide general information about the medicine {medicine}, "
                "including usage, precautions, and side effects."
            )
            response = get_ai_response(prompt)
            st.write(response)
            log_interaction(medicine, response)

# -----------------------------
# SECTION 12: EMERGENCY GUIDANCE
# -----------------------------

elif menu == "Emergency Guidance":
    st.subheader("🚨 Emergency Guidance")

    st.error("If this is a real emergency, call your local emergency number immediately.")

    issue = st.selectbox(
        "Select an emergency situation",
        [
            "Chest pain",
            "Breathing difficulty",
            "Severe bleeding",
            "Burn injury",
            "Unconsciousness",
            "High fever"
        ]
    )

    if st.button("Get Emergency Advice"):
        prompt = (
            f"Give first-aid guidance for {issue}. "
            "Include immediate steps and advise contacting emergency services."
        )
        response = get_ai_response(prompt)
        st.write(response)
        log_interaction(issue, response)

# -----------------------------
# SECTION 13: ABOUT
# -----------------------------

elif menu == "About":
    st.subheader("ℹ️ About")

    st.markdown(f"""
    **Application:** {APP_NAME}

    **Version:** {APP_VERSION}

    **Description:**
    Medi Buddy is an AI-powered medical awareness system developed as an academic project.
    It demonstrates the use of AI and cloud deployment in healthcare education.

    **Technologies Used:**
    - Python
    - Streamlit
    - OpenAI API

    **Note:**
    Voice features are available only in local execution due to cloud restrictions.
    """)

# -----------------------------
# SECTION 14: FOOTER
# -----------------------------

st.markdown("---")
st.caption("© 2026 Medi Buddy | Educational Use Only")

# -----------------------------
# END OF FILE
# -----------------------------
