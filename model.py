# model.py
# Simple ML-style disease prediction logic for Medi Buddy

def predict_disease(features):
    """
    features = [fever, cough, headache, fatigue]
    values are True / False
    """

    fever, cough, headache, fatigue = features

    if fever and cough and fatigue:
        return "Flu"

    if headache and not fever:
        return "Migraine"

    if fever and not cough:
        return "Viral Infection"

    if fatigue and headache:
        return "Stress or Weakness"

    return "Healthy / No Major Symptoms"
