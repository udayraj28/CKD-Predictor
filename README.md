CKD Predictor
A Flask-based web app that predicts Chronic Kidney Disease (CKD) using a trained machine learning model.

Overview
● Enter clinical parameters in a web form and receive a real-time CKD risk prediction.

● Preprocessing includes missing value handling, encoding categorical variables, and feature scaling.

● Simple, stateless, and ready for local deployment.

Features
● User-friendly web interface for inputting patient data (age, blood pressure, blood test results, etc.)

● Robust data preprocessing: handles missing values and encodes features before passing to the model.

● ML backend: Uses a scikit-learn model trained on CKD data, with model, scaler, and feature columns loaded at runtime.

● Instant results: Shows whether CKD is detected and suggests next steps.

Usage
Install dependencies bash pip install flask joblib numpy pandas scikit-learn

Directory structure text ckd-predictor/
│ 
├── app.py
├── models/ 
│      ├── ckd_model.pkl 
│      ├── scaler.pkl 
│      └── feature_columns.pkl
├── templates/ 
│      ├── index.html 
│      └── result.html 
├── static/ 
│      └── style.css
├── app.py

Run the app bash python app.py Open http://127.0.0.1:5000 in your browser.

Notes
● Ensure the ckd_model.pkl, scaler.pkl, and feature_columns.pkl files are present in the models/ folder.

● Model training and preprocessing were performed with scikit-learn using real CKD dataset features.

● This project is for educational use only.

Author: Uday Raj Sharma
