import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Sales Predictor Pro",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOGIN SYSTEM ---------------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 Login to Sales Predictor Pro")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
            st.rerun()
        else:
            st.error("Invalid Credentials ❌")

if not st.session_state.logged_in:
    login()
    st.stop()

# ---------------- LOAD MODEL ---------------- #
model = pickle.load(open("sales_model.pkl", "rb"))

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("⚙️ Control Panel")

items = st.sidebar.slider("📦 Items Sold", 0, 500, 100)
ad_budget = st.sidebar.slider("📢 Advertisement Budget", 0, 20000, 5000)
holiday = st.sidebar.selectbox("🎉 Holiday?", ["No", "Yes"])

holiday_value = 1 if holiday == "Yes" else 0

predict_button = st.sidebar.button("🚀 Predict")

# Logout button
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---------------- MAIN UI ---------------- #
st.title("📊 AI Sales Forecast Dashboard")

col1, col2 = st.columns(2)

# -------- Prediction Section -------- #
with col1:
    st.subheader("📈 Prediction Result")

    if predict_button:
        try:
            input_data = np.array([[items, ad_budget, holiday_value]])
            prediction = float(model.predict(input_data)[0])

            st.metric("Estimated Sales (₹)", f"{prediction:,.2f}")

            # Store prediction safely
            st.session_state.prediction = prediction

        except Exception as e:
            st.error("Prediction Error: Check model input format.")

# -------- Chart Section -------- #
with col2:
    st.subheader("📊 Live Sales Chart")

    if "prediction" in st.session_state:

        base_value = st.session_state.prediction

        # Ensure prediction is safe number
        if base_value <= 0:
            base_value = 100

        low = int(base_value * 0.7)
        high = int(base_value * 1.3)

        # Prevent randint crash
        if low >= high:
            high = low + 50

        sales_values = np.random.randint(low, high, 6)

        data = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Sales": sales_values
        })

        fig, ax = plt.subplots()
        ax.plot(data["Month"], data["Sales"], marker="o")
        ax.set_xlabel("Month")
        ax.set_ylabel("Sales")
        ax.set_title("Projected Monthly Sales Trend")

        st.pyplot(fig)

    else:
        st.info("Predict sales to see chart.")

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | AI Powered Dashboard")
