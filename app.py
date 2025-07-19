import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model
model = joblib.load("fraud_model.pkl")

# --- Page Config ---
st.set_page_config(page_title="💳 Fraud Detection App", layout="wide")

# --- Sidebar ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🔢 Predict via Input", "📁 Batch CSV Upload", "🧪 Use Sample Transaction"])

# --- Header ---
st.markdown("<h1 style='text-align: center;'>💳 Credit Card Fraud Detection</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Detect fraudulent transactions using a trained machine learning model.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Helper: Display Result ---
def display_result(pred, prob=None):
    if pred == 1:
        st.error("⚠️ **Fraudulent Transaction Detected!**")
    else:
        st.success("✅ **Legitimate Transaction**")

    if prob is not None:
        st.info(f"📈 **Fraud Probability**: `{prob:.2%}`")

# --- Page 1: Manual Input ---
if page == "🔢 Predict via Input":
    st.header("📝 Paste Comma-Separated Input")
    st.write("Enter 30 values separated by commas (Time, V1–V28, Amount):")

    raw_input = st.text_area("Input:", height=120, placeholder="e.g. 0.0, -1.3598, ..., 149.62")

    threshold = st.slider("🎯 Prediction Threshold", 0.0, 1.0, 0.5, 0.01)

    if st.button("🔍 Predict"):
        try:
            input_data = [float(x.strip()) for x in raw_input.split(",")]
            if len(input_data) != 30:
                st.warning("⚠️ Please enter exactly 30 values.")
            else:
                proba = model.predict_proba([input_data])[0][1]
                prediction = int(proba > threshold)
                display_result(prediction, proba)
        except Exception as e:
            st.error(f"❌ Invalid input: {e}")

# --- Page 2: CSV Upload ---
elif page == "📁 Batch CSV Upload":
    st.header("📤 Upload CSV File")
    uploaded_file = st.file_uploader("Upload a CSV file with 30 columns", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            if df.shape[1] < 30:
                st.warning("⚠️ The CSV must contain at least 30 columns.")
            else:
                input_data = df.iloc[:, :30]
                predictions = model.predict(input_data)
                proba = model.predict_proba(input_data)[:, 1]
                df['Prediction'] = predictions
                df['Fraud Probability'] = proba
                df['Label'] = df['Prediction'].map({0: 'Legitimate', 1: 'Fraud'})
                st.success("✅ Predictions generated!")
                st.dataframe(df)

                # Download
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download CSV with Predictions", data=csv, file_name="fraud_predictions.csv", mime="text/csv")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# --- Page 3: Sample Transaction ---
elif page == "🧪 Use Sample Transaction":
    st.header("🎯 Predict on a Sample Transaction")

    sample_input = [0.0, -1.35980713, -0.07278117, 2.53634674, 1.37815522,
                    -0.33832077, 0.46238778, 0.23959855, 0.0986979, 0.36378697,
                    0.09079417, -0.55159953, -0.61780086, -0.99138985, -0.31116935,
                    1.46817697, -0.47040053, 0.20797124, 0.02579058, 0.40399296,
                    0.2514121, -0.01830678, 0.27783757, -0.11047391, 0.06692807,
                    0.12853936, -0.18911484, 0.13355838, -0.02105305, 149.62]

    st.code(", ".join(str(round(x, 4)) for x in sample_input), language='text')
    
    if st.button("Predict Sample"):
        proba = model.predict_proba([sample_input])[0][1]
        prediction = int(proba > 0.5)
        display_result(prediction, proba)
