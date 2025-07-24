import streamlit as st
import pandas as pd
import pickle

# Load trained model
with open('taxi_out_time.pkl', 'rb') as f:
    model = pickle.load(f)

st.title("✈️ Taxi-Out Time Prediction App")

st.write("Fill in the flight and airport details to estimate taxi-out time (in minutes).")

# Input fields
dep_hour = st.number_input("Departure Hour (0–23)", min_value=0, max_value=23, step=1)
distance = st.number_input("Flight Distance (km)", min_value=0.0, step=10.0)
departing = st.number_input("Number of Departing Flights", min_value=0, step=1)
airline = st.selectbox("Airline", ["airline_a", "airline_b"])
runways = st.number_input("Runways Available", min_value=1, step=1)
weather = st.selectbox("Weather", ["Clear", "Rainy"])
weight = st.number_input("Aircraft Weight (kg)", min_value=1000, step=500)

# Encode categorical inputs
airline_code = 0 if airline == "airline_a" else 1
weather_code = 0 if weather == "Clear" else 1

# Predict button
if st.button("Predict Taxi-Out Time"):
    try:
        input_df = pd.DataFrame([[dep_hour, distance, departing, airline_code, runways, weather_code, weight]],
                                columns=['Departure_Hour', 'Flight_Distance_km', 'Departing_Flights',
                                         'Airline', 'Runways_Available', 'Weather', 'Aircraft_Weight_kg'])
        prediction = model.predict(input_df)
        st.success(f"Estimated Taxi-Out Time: {round(prediction[0], 2)} minutes")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
