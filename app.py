from flask import Flask, request, jsonify
import joblib, os, numpy as np
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Model load
model = joblib.load('phishing_model.pkl')
feature_names = None  # baad mein set hoga

@app.route('/')
def home():
    return jsonify({
        "project": "Cloud-Based Phishing Detection",
        "status": "running",
        "model": "Random Forest",
        "endpoints": ["/predict", "/health"]
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        features = np.array([list(data.values())])
        pred = model.predict(features)[0]
        conf = model.predict_proba(features)[0].max()
        result = "PHISHING" if pred == 1 else "LEGITIMATE"

        return jsonify({
            "result": result,
            "confidence": f"{conf*100:.1f}%",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)