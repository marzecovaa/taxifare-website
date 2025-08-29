import streamlit as st
import datetime
import pandas as pd
import json
import requests
import math

'''
# TaxiFareModel front
Exclaimer: This was vibe-coded from a simple layout to try out the capabilities of  v0.
Just wanted to try it out...

'''



# Set page configuration
st.set_page_config(
    page_title="Ride Fare Predictor",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .info-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🚕 TaxiFare Model Predictor</h1>', unsafe_allow_html=True)

st.markdown('''
This app allows you to predict taxi fares by entering trip details and submitting them to our prediction API.
Simply fill in the pickup and drop-off coordinates, select the date and passenger count, then click submit!
''')

# Create two main columns for better layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<h2 class="section-header">📅 Trip Details</h2>', unsafe_allow_html=True)

    # Pickup datetime with better default and validation
    pickup_datetime = st.date_input(
        "Pick-up Date",
        value=datetime.date.today(),
        min_value=datetime.date.today(),
        max_value=datetime.date.today() + datetime.timedelta(days=30),
        help="Select your desired pickup date"
    )

    # Passenger count with validation
    passenger_count = st.number_input(
        "Number of Passengers",
        min_value=1,
        max_value=8,
        value=1,
        step=1,
        help="How many passengers will be traveling?"
    )

with col2:
    st.markdown('<h2 class="section-header">📍 Location Details</h2>', unsafe_allow_html=True)

    # Pickup location section
    st.subheader("🟢 Pickup Location")
    pickup_col1, pickup_col2 = st.columns(2)

    with pickup_col1:
        pickup_latitude = st.number_input(
            "Pickup Latitude",
            value=40.7589,  # Default to NYC area
            min_value=-90.0,
            max_value=90.0,
            format="%.6f",
            help="Latitude coordinate for pickup location"
        )

    with pickup_col2:
        pickup_longitude = st.number_input(
            "Pickup Longitude",
            value=-73.9851,  # Default to NYC area
            min_value=-180.0,
            max_value=180.0,
            format="%.6f",
            help="Longitude coordinate for pickup location"
        )

    # Dropoff location section
    st.subheader("🔴 Drop-off Location")
    dropoff_col1, dropoff_col2 = st.columns(2)

    with dropoff_col1:
        dropoff_latitude = st.number_input(
            "Drop-off Latitude",
            value=40.7505,  # Default to NYC area
            min_value=-90.0,
            max_value=90.0,
            format="%.6f",
            help="Latitude coordinate for drop-off location"
        )

    with dropoff_col2:
        dropoff_longitude = st.number_input(
            "Drop-off Longitude",
            value=-73.9934,  # Default to NYC area
            min_value=-180.0,
            max_value=180.0,
            format="%.6f",
            help="Longitude coordinate for drop-off location"
        )

st.markdown('<h2 class="section-header">🗺️ Trip Route Visualization</h2>', unsafe_allow_html=True)

# Create DataFrame for map points
map_data = pd.DataFrame({
    'lat': [pickup_latitude, dropoff_latitude],
    'lon': [pickup_longitude, dropoff_longitude],
    'type': ['Pickup', 'Dropoff'],
    'color': ['#00ff00', '#ff0000']  # Green for pickup, red for dropoff
})

# Calculate and display distance
def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on earth (in km)"""
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

distance = calculate_distance(pickup_latitude, pickup_longitude, dropoff_latitude, dropoff_longitude)

# Display map and trip info
map_col1, map_col2 = st.columns([3, 1])

with map_col1:
    st.map(map_data, size=20, color='color')

    # Add location details below the map
    st.markdown("**📍 Location Details:**")
    col_pickup, col_dropoff = st.columns(2)

    with col_pickup:
        st.markdown(f"""
        **🟢 Pickup Location**
        - Lat: {pickup_latitude:.6f}
        - Lon: {pickup_longitude:.6f}
        """)

    with col_dropoff:
        st.markdown(f"""
        **🔴 Drop-off Location**
        - Lat: {dropoff_latitude:.6f}
        - Lon: {dropoff_longitude:.6f}
        """)

with map_col2:
    st.metric("📏 Trip Distance", f"{distance:.2f} km")
    st.metric("📏 Trip Distance", f"{distance * 0.621371:.2f} miles")

    # Trip summary
    st.markdown("**Trip Summary:**")
    st.write(f"🟢 From: ({pickup_latitude:.4f}, {pickup_longitude:.4f})")
    st.write(f"🔴 To: ({dropoff_latitude:.4f}, {dropoff_longitude:.4f})")
    st.write(f"👥 Passengers: {passenger_count}")
    st.write(f"📅 Date: {pickup_datetime}")

st.markdown('<h2 class="section-header">⚙️ API Configuration</h2>', unsafe_allow_html=True)
api_url = st.text_input(
    "API Endpoint URL",
    value="https://taxifare-404340875274.europe-west1.run.app/predict",
    help="Enter the API endpoint URL for fare prediction"
)

button_col1, button_col2, button_col3 = st.columns([1, 2, 1])

with button_col2:
    if st.button("🚀 Get Fare Prediction", type="primary", use_container_width=True):
        payload = {
            "pickup_datetime": pickup_datetime.isoformat(),
            "pickup_latitude": pickup_latitude,
            "pickup_longitude": pickup_longitude,
            "dropoff_latitude": dropoff_latitude,
            "dropoff_longitude": dropoff_longitude,
            "passenger_count": passenger_count
        }

        # Display the payload being sent
        st.markdown('<h3 class="section-header">📤 Request Payload</h3>', unsafe_allow_html=True)
        st.json(payload)

        with st.spinner("🔄 Getting fare prediction..."):
            success = False

            # Method 1: Try GET request with query parameters
            try:
                st.info("🔄 Trying GET request with query parameters...")
                params = {
                    "pickup_datetime": pickup_datetime.isoformat(),
                    "pickup_latitude": pickup_latitude,
                    "pickup_longitude": pickup_longitude,
                    "dropoff_latitude": dropoff_latitude,
                    "dropoff_longitude": dropoff_longitude,
                    "passenger_count": passenger_count
                }

                response = requests.get(
                    api_url,
                    params=params,
                    timeout=30
                )

                if response.status_code == 200:
                    success = True
                    st.success("✅ Prediction received successfully with GET request!")
                else:
                    st.warning(f"GET request failed with status: {response.status_code}")

            except Exception as e:
                st.warning(f"GET request failed: {str(e)}")

            # Method 2: Try POST with JSON if GET failed
            if not success:
                try:
                    st.info("🔄 Trying POST request with JSON body...")
                    headers = {
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    }

                    response = requests.post(
                        api_url,
                        json=payload,
                        headers=headers,
                        timeout=30
                    )

                    if response.status_code == 200:
                        success = True
                        st.success("✅ Prediction received successfully with POST request!")
                    else:
                        st.warning(f"POST JSON request failed with status: {response.status_code}")

                except Exception as e:
                    st.warning(f"POST JSON request failed: {str(e)}")

            # Method 3: Try POST with form data if JSON failed
            if not success:
                try:
                    st.info("🔄 Trying POST request with form data...")
                    response = requests.post(
                        api_url,
                        data=payload,
                        timeout=30
                    )

                    if response.status_code == 200:
                        success = True
                        st.success("✅ Prediction received successfully with form data!")
                    else:
                        st.warning(f"POST form data request failed with status: {response.status_code}")

                except Exception as e:
                    st.warning(f"POST form data request failed: {str(e)}")

            # Display results if any method succeeded
            if success:
                st.balloons()

                st.markdown('<h3 class="section-header">📋 API Response</h3>', unsafe_allow_html=True)

                try:
                    response_data = response.json()
                    st.json(response_data)

                    # Try different possible response keys
                    fare_value = None
                    if 'fare' in response_data:
                        fare_value = response_data['fare']
                    elif 'prediction' in response_data:
                        fare_value = response_data['prediction']
                    elif 'predicted_fare' in response_data:
                        fare_value = response_data['predicted_fare']
                    elif isinstance(response_data, (int, float)):
                        fare_value = response_data

                    if fare_value is not None:
                        st.metric(
                            label="💰 Predicted Fare",
                            value=f"${float(fare_value):.2f}"
                        )
                    else:
                        st.info("💡 Prediction received but fare value format not recognized")

                except json.JSONDecodeError:
                    st.warning("⚠️ Response is not valid JSON")
                    st.text_area("Raw Response", response.text, height=200)

            else:
                st.error("❌ All request methods failed. Please check:")
                st.markdown("""
                - ✅ API endpoint URL is correct
                - ✅ API server is running and accessible
                - ✅ API accepts the expected request format
                - ✅ Network connection is stable
                """)

                # Show the last response for debugging
                if 'response' in locals():
                    st.text_area("Last Error Response", response.text, height=100)

st.markdown('<h2 class="section-header">ℹ️ How it Works</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="info-box">
<strong>This app predicts taxi fares using machine learning:</strong>
<ul>
<li>📍 Enter pickup and drop-off coordinates</li>
<li>📅 Select your travel date</li>
<li>👥 Specify number of passengers</li>
<li>🚀 Submit to get an instant fare prediction</li>
</ul>
</div>
""", unsafe_allow_html=True)
