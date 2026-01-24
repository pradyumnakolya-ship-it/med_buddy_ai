# model.py
# Cloud-safe disease prediction logic for Medi Buddy

def predict_disease(features):
    """
    Predict disease based on symptom inputs.
    features: [fever, cough, headache, fatigue]
    Each value is True or False
    """

    fever, cough, headache, fatigue = features

    if fever and cough and fatigue:
        return "Flu"

    if fever and cough:
        return "Viral Infection"

    if headache and not fever:
        return "Migraine"

    if fatigue and headache:
        return "Stress or Weakness"

    if fever:
        return "Mild Fever"

    return "No Major Illness Detected"
