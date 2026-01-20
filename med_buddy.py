import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Medi Buddy",
    page_icon="🩺",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("🩺 Medi Buddy")
st.caption("Cloud-deployed, offline medical awareness assistant")

st.warning(
    "⚠ DISCLAIMER: This application is for educational and informational purposes only. "
    "It does NOT diagnose diseases or prescribe treatment. "
    "Always consult a qualified healthcare professional."
)

# ---------------- SIDEBAR ----------------
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

# ---------------- RULE-BASED LOGIC ----------------
def symptom_checker(symptoms):
    symptoms = symptoms.lower()

    if "fever" in symptoms and "cough" in symptoms:
        return (
            "Possible Condition: Viral Infection / Flu\n\n"
            "General Advice:\n"
            "- Take rest\n"
            "- Drink warm fluids\n"
            "- Monitor temperature\n"
            "- Consult a doctor if symptoms persist"
        )

    if "headache" in symptoms:
        return (
            "Possible Cause: Stress / Dehydration / Migraine\n\n"
            "General Advice:\n"
            "- Stay hydrated\n"
            "- Rest in a quiet room\n"
            "- Avoid screen strain"
        )

    return (
        "Your symptoms are not clearly identifiable.\n\n"
        "Please consult a healthcare professional for accurate guidance."
    )


def disease_info(disease):
    disease = disease.lower()

    if disease == "diabetes":
        return (
            "Diabetes is a chronic condition affecting blood sugar levels.\n\n"
            "Common Symptoms:\n"
            "- Increased thirst\n"
            "- Frequent urination\n"
            "- Fatigue\n\n"
            "Management:\n"
            "- Healthy diet\n"
            "- Regular exercise\n"
            "- Medical supervision"
        )

    return "Disease information not found."


def medicine_info(medicine):
    medicine = medicine.lower()

    if medicine == "paracetamol":
        return (
            "Paracetamol is used to relieve pain and reduce fever.\n\n"
            "Note:\n"
            "- Do not exceed recommended dosage\n"
            "- Consult a doctor if unsure"
        )

    return "Medicine information not found."


# ---------------- PAGES ----------------
if menu == "Home":
    st.subheader("Welcome 👋")
    st.write(
        "Medi Buddy helps users understand basic medical information, "
        "symptoms, medicines, and emergency steps using offline logic."
    )

elif menu == "Symptom Checker":
    st.subheader("🧪 Symptom Checker")
    user_symptoms = st.text_area("Describe your symptoms")

    if st.button("Analyze Symptoms"):
        if user_symptoms.strip():
            result = symptom_checker(user_symptoms)
            st.success(result)
        else:
            st.error("Please enter your symptoms.")

elif menu == "Disease Information":
    st.subheader("📖 Disease Information")
    disease = st.text_input("Enter disease name")

    if st.button("Get Disease Info"):
        if disease.strip():
            st.info(disease_info(disease))
        else:
            st.error("Please enter a disease name.")

elif menu == "Medicine Information":
    st.subheader("💊 Medicine Information")
    medicine = st.text_input("Enter medicine name")

    if st.button("Get Medicine Info"):
        if medicine.strip():
            st.info(medicine_info(medicine))
        else:
            st.error("Please enter a medicine name.")

elif menu == "Emergency Guidance":
    st.subheader("🚨 Emergency Guidance")
    st.error(
        "If this is a medical emergency:\n\n"
        "📞 Call local emergency services immediately.\n"
        "🏥 Visit the nearest hospital."
    )

elif menu == "About":
    st.subheader("ℹ About Medi Buddy")
    st.write(
        "Medi Buddy is an AI-inspired, rule-based medical awareness system "
        "developed for academic purposes.\n\n"
        "© 2026 Medi Buddy | Educational Use Only"
    )
