import streamlit as st
import pandas as pd
import os
import cloudpickle
import gdown

# Download model if not exists
FILE_ID = "1gatdvbTPXR1C2EDvYU26THcvAGIvoQbx"
MODEL_PATH = "credit_card_fraud_model.pkl"

def download_model():
    url = f"https://drive.google.com/uc?id={FILE_ID}"
    gdown.download(url, MODEL_PATH, quiet=False)

if not os.path.exists(MODEL_PATH):
    with st.spinner('Downloading the model... Please wait ⏳'):
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

st.set_page_config(
    page_title="💳 Credit Card Fraud Detection",
    page_icon="🚨",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
        padding: 2rem 4rem 4rem 4rem;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgb(0 0 0 / 0.12);
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        height: 3rem;
        width: 100%;
        font-size: 18px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ff2a2a;
        color: white;
    }
    .stSelectbox>div>div>div>select {
        font-weight: 600;
        font-size: 16px;
        padding: 0.4rem;
    }
    .stNumberInput>div>input {
        font-size: 16px;
        font-weight: 600;
        padding: 0.5rem;
    }
    h1 {
        color: #FF4B4B;
        font-weight: 700;
    }
    .prediction {
        font-size: 20px;
        font-weight: 700;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>💳 Swipe Shield</h1>", unsafe_allow_html=True)
st.markdown("### Enter the transaction details below to check for fraud.")

with st.form(key="fraud_form"):
    col1, col2 = st.columns(2)

    with col1:
        transaction_type = st.selectbox(
            "Transaction Type", ['PAYMENT', 'CASH_OUT', 'TRANSFER', 'DEPOSIT']
        )
        amount = st.number_input(
            "Transaction Amount", min_value=0.0, value=1000.0, step=1.0, format="%.2f"
        )
        oldbalanceOrg = st.number_input(
            "Sender's Old Balance", min_value=0.0, value=5000.0, step=1.0, format="%.2f"
        )
    
    with col2:
        newbalanceOrig = st.number_input(
            "Sender's New Balance", min_value=0.0, value=4000.0, step=1.0, format="%.2f"
        )
        oldbalanceDest = st.number_input(
            "Receiver's Old Balance", min_value=0.0, value=1000.0, step=1.0, format="%.2f"
        )
        newbalanceDest = st.number_input(
            "Receiver's New Balance", min_value=0.0, value=2000.0, step=1.0, format="%.2f"
        )

    submitted = st.form_submit_button("🚨 Predict Fraud")

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

        # Suspicious pattern detection
        suspicious = []
        if amount == 0:
            suspicious.append("Amount is $0.00")
        if newbalanceOrig == oldbalanceOrg:
            suspicious.append("Sender's balance did not change")
        if newbalanceDest == oldbalanceDest:
            suspicious.append("Receiver's balance did not change")

        # Result box
        if prediction[0] == 1:
            st.error("⚠️ Fraudulent Transaction Detected!")
        else:
            st.success("✅ Legitimate Transaction")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
