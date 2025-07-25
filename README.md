# 💳 Swipe Shield – Credit Card Fraud Detection System

🚀 **June 2025 – July 2025**  
🔗 [GitHub](https://github.com/chiragmiyy/Credit-Card-Fraud-Detection-System) | [WebApp](https://credit-card-fraud-detection-system-chiragmiyy.streamlit.app)  
📌 *Machine Learning · Python · Scikit-learn · Streamlit · Pandas*

---

## 🧠 Overview

Swipe Shield is a machine learning-powered credit card fraud detection system built using a highly imbalanced dataset (only 0.17% fraud cases). The system is capable of identifying fraudulent transactions based on anonymized features using multiple classification models.

A user-friendly **Streamlit web application** allows users to simulate transaction inputs and receive real-time fraud predictions.

---

## 🚀 Features

- ⚡ **Accurate Fraud Detection** on an imbalanced dataset  
- 🌐 **Live Web Application** powered by Streamlit  
- 💾 **Model Serialization** with `cloudpickle` for production-grade deployment  
- 📈 **Interactive Inputs** to simulate real-time credit card transactions  
- ☁️ **Google Drive Integration** for dynamic model loading  

---

## 🛠️ Tech Stack

- **Languages & Frameworks**: Python, Streamlit  
- **Libraries**: Scikit-learn, Pandas, Numpy, cloudpickle  
- **Deployment**: Streamlit Cloud, Google Drive  

---

## 📥 Installation

To run the app locally:

```bash
# Clone the repository
git clone https://github.com/chiragmiyy/Credit-Card-Fraud-Detection-System.git
cd Credit-Card-Fraud-Detection-System

# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 🧪 Usage

Once the app is running, you'll be prompted to enter transaction details such as:

- **Time**  
- **Amount**  
- **V1 to V28** (anonymized PCA components)

After submitting the input, the model returns a prediction:

- ⚠️ **Fraud Detected!**  
- ✅ **Transaction is Safe!**

> The model is dynamically loaded from a cloudpickle file hosted via Google Drive.

---

## 📸 Demo

Real-time fraud prediction with user input simulation.

📌 *Don't have a screenshot? You can take one using `Cmd+Shift+4` on macOS or `Snipping Tool` on Windows and place it in a `screenshots/` folder.*

---

## 📁 Project Structure

```
.
├── app.py                 # Streamlit frontend for user input & prediction
├── model.pkl              # Serialized ML model (cloudpickled)
├── fraud_detection.py     # Model training & evaluation scripts
├── utils.py               # Utility functions
├── requirements.txt       # List of dependencies
└── README.md              # Project documentation
```

---

## 📊 Dataset

- **Source**: [Kaggle - Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)  
- Contains transactions made by European cardholders in September 2013  
- Features are anonymized (`V1` to `V28`) using PCA  

---

## 🙌 Acknowledgments

- ULB Machine Learning Group for the dataset  
- Streamlit team for an amazing deployment tool  

---

## 📫 Contact

Feel free to connect or reach out for collaborations:

- 🔗 GitHub: [chiragmiyy](https://github.com/chiragmiyy)  
- 📧 Email: chirag.agr06@gmail.com
