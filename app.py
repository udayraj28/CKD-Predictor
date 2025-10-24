from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Load model, scaler, and feature columns
model = joblib.load('models/ckd_model.pkl')
scaler = joblib.load('models/scaler.pkl')
fields = joblib.load('models/feature_columns.pkl')

# Remove unwanted columns like 'id' if present
if 'id' in fields:
    fields.remove('id')

def get_risk_feedback(probability, lab_values, predicted_class):
    """
    Parameters:
        probability: float, model-predicted probability of CKD (from predict_proba, 0–1)
        lab_values: dict, keys: 'sc' (creatinine), 'hemo' (hemoglobin), 'al' (albumin)
        predicted_class: int, model output (1 for CKD, 0 for No CKD)
    Returns:
        (risk_level, ckd_stage) as strings
    """
    sc = lab_values.get('sc', None)
    hemo = lab_values.get('hemo', None)
    al = lab_values.get('al', None)

    if predicted_class == 0:
        return "No CKD detected", "No CKD"

    risk_level = "Low risk"
    ckd_stage = "No CKD or early stage"

    if probability > 0.95:
        risk_level = "High risk"
    elif probability > 0.75:
        risk_level = "Moderate risk"
    else:
        risk_level = "Low risk"

    if sc is not None and hemo is not None:
        if sc < 1.5 and hemo > 12:
            ckd_stage = "Likely Stage 1 or 2 CKD"
        elif 1.5 <= sc < 3.0 or (10 <= hemo <= 12):
            ckd_stage = "Likely Stage 3 CKD"
        elif sc >= 3.0 or hemo < 10:
            ckd_stage = "Likely Stage 4 or 5 CKD"

    if al is not None and al >= 3:
        ckd_stage += ", with significant albuminuria"

    return risk_level, ckd_stage

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = []
        user_id = request.form.get('id', None)

        for field in fields:
            val = request.form.get(field)
            if val is None or val == '':
                return f"Missing input for {field}", 400
            input_data.append(float(val))

        input_df = pd.DataFrame([input_data], columns=fields)

        input_scaled = scaler.transform(input_df)

        prediction = model.predict(input_scaled)[0]
        pred_proba = model.predict_proba(input_scaled)[0][1]

        lab_vals = {
            'sc': input_df['sc'].values[0] if 'sc' in input_df.columns else None,
            'hemo': input_df['hemo'].values[0] if 'hemo' in input_df.columns else None,
            'al': input_df['al'].values[0] if 'al' in input_df.columns else None,
        }

        # Pass prediction as the third argument
        risk, stage = get_risk_feedback(pred_proba, lab_vals, prediction)

        if prediction == 1:
            result = f"🩺 CKD Detected – Please consult a nephrologist.<br><b>{risk}</b><br><b>{stage}</b>"
        else:
            result = f"✅ No CKD Detected – Keep up the healthy lifestyle!<br><b>{risk}</b><br><b>{stage}</b>"

        return render_template('result.html', result=result, user_id=user_id)

    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == '__main__':
    # Use the PORT environment variable provided by Render, or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Listen on all interfaces (0.0.0.0) instead of just localhost
    app.run(host='0.0.0.0', port=port, debug=False)