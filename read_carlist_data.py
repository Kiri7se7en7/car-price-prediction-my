import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load the CSV file
df = pd.read_csv("carlist_data.csv")

# --- Data Cleaning Functions ---

def clean_price(price):
    """Extract numerical price from string and convert to float."""
    match = re.search(r"\d[\d,]*", str(price))  # Find first number sequence
    return float(match.group(0).replace(",", "")) if match else None  # Remove commas & convert

df["Price"] = df["Price"].apply(clean_price)

def clean_mileage(mileage):
    """Convert mileage with 'K' (thousands) into actual numbers."""
    if isinstance(mileage, str):
        matches = re.findall(r"(\d+)(K?)", mileage)
        numbers = [int(num) * (1000 if k else 1) for num, k in matches]

        if len(numbers) == 2:  # If range (e.g., "5 - 10K KM"), take average
            return np.mean(numbers)
        elif len(numbers) == 1:
            return numbers[0]
    return None  # Return None if no valid number found

df["Mileage"] = df["Mileage"].apply(clean_mileage)

# Drop missing values
df.dropna(inplace=True)

# --- Data Visualization ---

plt.figure(figsize=(10, 6))
sns.scatterplot(x=df["Mileage"], y=df["Price"])
plt.xlabel("Mileage (km)")
plt.ylabel("Price (RM)")
plt.title("Mileage vs Price")
plt.xticks(rotation=45)
plt.ticklabel_format(style="plain", axis="y")
plt.show()

if "Transmission" in df.columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df["Transmission"], y=df["Price"])
    plt.xlabel("Transmission")
    plt.ylabel("Price (RM)")
    plt.title("Car Price by Transmission Type")
    plt.ticklabel_format(style="plain", axis="y")
    plt.show()
else:
    print("Transmission data not found in dataset!")

# --- Data Preprocessing ---

# Encode Transmission (Manual = 0, Automatic = 1)
df["Transmission"] = df["Transmission"].astype("category").cat.codes

# Encode Location
df["Location"] = df["Location"].astype("category")

# Save the location encoding for later use in Streamlit app
location_mapping = {name: code for code, name in enumerate(df["Location"].cat.categories)}

with open("location_mapping.pkl", "wb") as file:
    pickle.dump(location_mapping, file)  # ✅ Stores names as keys, numbers as values

print("✔️ Location mapping saved:", location_mapping)

# Convert Location column to numerical values
df["Location"] = df["Location"].cat.codes  # Convert to categorical codes

# Define features (X) and target (y)
X = df[["Mileage", "Transmission", "Location"]]
y = df["Price"]

# Split dataset: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Model Training & Evaluation ---

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on test data
y_pred = model.predict(X_test)

# Model Performance Metrics
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Model Performance:\nMAE: {mae:.2f}\nMSE: {mse:.2f}\nR² Score: {r2:.4f}")

# Save the trained model
with open("car_price_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("✔️ Model & location mapping saved successfully!")
