import streamlit as st
import requests

st.set_page_config(page_title="House Price Predictor")

st.title("🏠 House Price Prediction App")

# Input fields
area = st.number_input("Area (in sq ft)", min_value=100, max_value=10000, value=1000)
bedrooms = st.number_input("Number of Bedrooms", min_value=1, max_value=10, value=3)
bathrooms = st.number_input("Number of Bathrooms", min_value=1, max_value=10, value=2)
stories = st.number_input("Number of Stories", min_value=1, max_value=4, value=1)

mainroad = st.selectbox("Main Road Access", ["yes", "no"])
guestroom = st.selectbox("Guest Room Available", ["yes", "no"])
basement = st.selectbox("Basement Available", ["yes", "no"])
hotwaterheating = st.selectbox("Hot Water Heating", ["yes", "no"])
airconditioning = st.selectbox("Air Conditioning", ["yes", "no"])
parking = st.number_input("Parking Spaces", min_value=0, max_value=5, value=1)
prefarea = st.selectbox("In Preferred Area", ["yes", "no"])
furnishingstatus = st.selectbox("Furnishing Status", ["unfurnished", "semi-furnished", "furnished"])

# Convert categorical fields to numerical
def encode_yes_no(value):
    return 1 if value == "yes" else 0

furnish_map = {
    "unfurnished": 0,
    "semi-furnished": 1,
    "furnished": 2
}

# Predict button
if st.button("Predict Price"):
    payload = {
        "area": area,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "stories": stories,
        "mainroad": encode_yes_no(mainroad),
        "guestroom": encode_yes_no(guestroom),
        "basement": encode_yes_no(basement),
        "hotwaterheating": encode_yes_no(hotwaterheating),
        "airconditioning": encode_yes_no(airconditioning),
        "parking": parking,
        "prefarea": encode_yes_no(prefarea),
        "furnishingstatus": furnish_map[furnishingstatus]
    }

    try:
        response = requests.post("https://house-prediction-api.onrender.com/predict", json=payload)
        result = response.json()

        if "predicted_price" in result:
            st.success(f"🏷️ Predicted Price: ${result['predicted_price']:.2f}")
        else:
            st.error(f"❌ Error: {result.get('error', 'Unknown error')}")

    except Exception as e:
        st.error(f"⚠️ Could not connect to backend. Error: {e}")
