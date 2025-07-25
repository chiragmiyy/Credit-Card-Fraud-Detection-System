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
    with st.spinner('📦 Downloading the model...'):
        download_model()

# Fix for column transformer compatibility
from sklearn.compose import _column_transformer
class _RemainderColsList(list): pass
_column_transformer._RemainderColsList = _RemainderColsList

try:
    with open(MODEL_PATH, "rb") as f:
        model = cloudpickle.load(f)
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Page config
st.set_page_config(
    page_title="💳 Credit Card Fraud Detection",
    page_icon="🚨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Inject custom CSS
st.markdown("""
<style>
    body {
        font-family: 'Segoe UI', sans-serif;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem 3rem;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3rem;
        width: 100%;
        font-size: 17px;
        border: none;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #e63946;
        transform: scale(1.02);
    }
    .stSelectbox label, .stNumberInput label {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    h1, h3 {
        color: #FF4B4B;
        font-weight: 800;
    }
    .prediction-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-left: 5px solid #ffc107;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>💳 Swipe Shield</h1>", unsafe_allow_html=True)
st.markdown("##### Enter transaction details to check if it's fraudulent:")

# Form layout
with st.form(key="fraud_form"):
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            transaction_type = st.selectbox(
                "Transaction Type", ['PAYMENT', 'CASH_OUT', 'TRANSFER', 'DEPOSIT']
            )
            amount = st.number_input(
                "Transaction Amount (USD)", min_value=0.0, value=1000.0, step=1.0, format="%.2f"
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

# Prediction logic
if submitted:
    try:
        input_data = pd.DataFrame([{
            'type': transaction_type,
            'amount': amount,
            'oldbalanceOrg': oldbalanceOrg,
            'newbalanceOrig': newbalanceOrig,
            'oldbalanceDest': oldbalanceDest,
            'newbalanceDest': newbalanceDest
        }])

        prediction = model.predict(input_data)

        if prediction[0] == 1:
            st.markdown(
                '<div class="prediction-box" style="border-left-color:#dc3545;background-color:#f8d7da;">⚠️ <strong>Fraudulent Transaction Detected!</strong></div>',
                unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="prediction-box" style="border-left-color:#28a745;background-color:#d4edda;">✅ <strong>Legitimate Transaction</strong></div>',
                unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Prediction failed: {e}")
