import streamlit as st
import pandas as pd
import os
import cloudpickle
import gdown

FILE_ID = "1gatdvbTPXR1C2EDvYU26THcvAGIvoQbx"
MODEL_PATH = "credit_card_fraud_model.pkl"

def download_model():
    url = f"https://drive.google.com/uc?id={FILE_ID}"
    gdown.download(url, MODEL_PATH, quiet=False)

if not os.path.exists(MODEL_PATH):
    with st.spinner('📦 Downloading model...'):
        download_model()

from sklearn.compose import _column_transformer
class _RemainderColsList(list): pass
_column_transformer._RemainderColsList = _RemainderColsList

try:
    with open(MODEL_PATH, "rb") as f:
        model = cloudpickle.load(f)
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

st.set_page_config(page_title="Swipe Shield", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, .main {
    background: #0f1117;
    color: #ffffff;
    font-family: 'Inter', sans-serif;
}

h1 {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.2em;
}

h3 {
    text-align: center;
    font-weight: 400;
    color: #aaaaaa;
    margin-bottom: 2.5em;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 30px;
    border-radius: 16px;
    max-width: 950px;
    margin: auto;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.08);
}

.stNumberInput>div>input, .stSelectbox>div>div>div {
    background-color: #1e1e2f !important;
    color: white !important;
    border-radius: 8px !important;
}

.stButton>button {
    background-color: #ff4b4b;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    font-size: 16px;
    padding: 12px 24px;
    margin-top: 20px;
    width: 100%;
    transition: 0.3s;
    border: none;
}

.stButton>button:hover {
    background-color: #e63946;
    transform: scale(1.02);
}

.result {
    margin-top: 30px;
    padding: 20px;
    text-align: left;
    border-radius: 12px;
    font-size: 18px;
    font-weight: 500;
    line-height: 1.7;
}

.fraud {
    background: #2b1a1a;
    color: #ffb3b3;
    border-left: 6px solid #ff4b4b;
}

.legit {
    background: #1a2b1a;
    color: #b2f5b2;
    border-left: 6px solid #4caf50;
}

.warning {
    background-color: #332f1f;
    padding: 15px;
    border-left: 6px solid #ffc107;
    border-radius: 10px;
    margin-top: 15px;
    color: #fce8b2;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>💳 Swipe Shield</h1>", unsafe_allow_html=True)
st.markdown("<h3>AI-powered Credit Card Fraud Detection</h3>", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)

with st.form("fraud_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        transaction_type = st.selectbox("Transaction Type", ['PAYMENT', 'CASH_OUT', 'TRANSFER', 'DEPOSIT'])
        amount = st.number_input("Amount (USD)", min_value=0.0, value=1000.0, format="%.2f")
    with col2:
        oldbalanceOrg = st.number_input("Sender's Old Balance", min_value=0.0, value=5000.0, format="%.2f")
        newbalanceOrig = st.number_input("Sender's New Balance", min_value=0.0, value=4000.0, format="%.2f")
    with col3:
        oldbalanceDest = st.number_input("Receiver's Old Balance", min_value=0.0, value=1000.0, format="%.2f")
        newbalanceDest = st.number_input("Receiver's New Balance", min_value=0.0, value=2000.0, format="%.2f")

    submitted = st.form_submit_button("🚨 Predict Fraud")

st.markdown('</div>', unsafe_allow_html=True)

if submitted:
    input_data = pd.DataFrame([{
        'type': transaction_type,
        'amount': amount,
        'oldbalanceOrg': oldbalanceOrg,
        'newbalanceOrig': newbalanceOrig,
        'oldbalanceDest': oldbalanceDest,
        'newbalanceDest': newbalanceDest
    }])

    try:
        prediction = model.predict(input_data)
        proba = model.predict_proba(input_data)[0][1] * 100  # Confidence in class 1 (fraud)

        suspicious = []
        if amount == 0:
            suspicious.append("Amount is $0.00")
        if newbalanceOrig == oldbalanceOrg:
            suspicious.append("Sender's balance did not change")
        if newbalanceDest == oldbalanceDest:
            suspicious.append("Receiver's balance did not change")

        if prediction[0] == 1:
            st.markdown(f"""
            <div class="result fraud">
                ⚠️ <strong>Fraudulent Transaction Detected!</strong><br><br>
                🔒 <strong>Type:</strong> {transaction_type} &nbsp;|&nbsp;
                💵 <strong>Amount:</strong> ${amount:,.2f}<br>
                📊 <strong>Model Confidence:</strong> {proba:.2f}%<br>
                💳 <strong>Sender:</strong> ${oldbalanceOrg:,.2f} → ${newbalanceOrig:,.2f}<br>
                🧾 <strong>Receiver:</strong> ${oldbalanceDest:,.2f} → ${newbalanceDest:,.2f}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result legit">
                ✅ <strong>Legitimate Transaction</strong><br><br>
                🔒 <strong>Type:</strong> {transaction_type} &nbsp;|&nbsp;
                💵 <strong>Amount:</strong> ${amount:,.2f}<br>
                📊 <strong>Model Confidence:</strong> {proba:.2f}%<br>
                💳 <strong>Sender:</strong> ${oldbalanceOrg:,.2f} → ${newbalanceOrig:,.2f}<br>
                🧾 <strong>Receiver:</strong> ${oldbalanceDest:,.2f} → ${newbalanceDest:,.2f}
            </div>
            """, unsafe_allow_html=True)

        # Suspicious notes
        if suspicious:
            st.markdown(f"""
            <div class="warning">
                ⚠️ <strong>Suspicious Behavior Detected:</strong><br>
                {"<br>".join(["• " + s for s in suspicious])}
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Prediction failed: {e}")