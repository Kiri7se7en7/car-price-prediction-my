import numpy as np
import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load trained model
try:
    with open("car_price_model.pkl", "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error("🚨 Model file not found! Please check 'car_price_model.pkl'.")
    model = None  # Set to None if not found

# Load location mapping
try:
    with open("location_mapping.pkl", "rb") as file:
        location_mapping = pickle.load(file)  # ✅ This now contains names as keys
except FileNotFoundError:
    st.error("🚨 Location mapping file not found! Please check 'location_mapping.pkl'.")
    location_mapping = {}

# Get list of location names (if available)
location_names = sorted(location_mapping.keys()) if location_mapping else []

# Streamlit UI
st.set_page_config(page_title="Car Price Prediction", page_icon="🚗", layout="wide")
st.title("🚗 Car Price Prediction App")

# Create columns for a cleaner layout
col1, col2, col3 = st.columns(3)

with col1:
    mileage = st.number_input("📏 Enter Mileage (km)", min_value=0, step=1000, value=50000)

with col2:
    transmission = st.selectbox("🛠️ Transmission Type", ["Manual", "Automatic"])

with col3:
    if location_names:
        selected_location_name = st.selectbox("📍 Select Location", location_names)
        location_value = location_mapping[selected_location_name]  # Get encoded location
    else:
        st.warning("⚠️ No location data found. Using default location (0).")
        location_value = 0

# Convert transmission to numerical value
transmission_map = {"Manual": 0, "Automatic": 1}
transmission_value = transmission_map[transmission]

if st.button("🔍 Predict Price"):
    if model:
        try:
            # Prepare input data
            input_data = np.array([[mileage, transmission_value, location_value]], dtype=float)

            # Make prediction
            prediction = model.predict(input_data)

            # Display result
            st.success(f"💰 Estimated Price: **RM {prediction[0]:,.2f}**")
        except Exception as e:
            st.error(f"❌ Error during prediction: {e}")
    else:
        st.error("❌ Model not loaded. Check the 'car_price_model.pkl' file.")

# Load dataset
try:
    df = pd.read_csv("carlist_data.csv")
except FileNotFoundError:
    st.error("🚨 Data file not found! Please check 'carlist_data.csv'.")
    df = None

st.header("📊 Car Price Analysis")

if df is not None:
    # Scatter Plot: Mileage vs Price
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x=df["Mileage"], y=df["Price"], ax=ax)
    plt.xlabel("Mileage (km)")
    plt.ylabel("Price (RM)")
    plt.title("Mileage vs Price")
    st.pyplot(fig)

    # Histogram: Price Distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["Price"], bins=20, kde=True, ax=ax)
    plt.xlabel("Price (RM)")
    plt.title("Car Price Distribution")
    st.pyplot(fig)
else:
    st.warning("No data available for visualization.")
