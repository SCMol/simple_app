import streamlit as st
import requests
import base64

# Load and set the background image
import streamlit as st
import requests
import base64

import streamlit as st
import requests
import base64

# Load and set the background image
def set_bg(path):
    with open(path, "rb") as file:
        base64_img = base64.b64encode(file.read()).decode("utf-8")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/webp;base64,{base64_img}");
            background-size: cover;
        }}
        .sidebar .sidebar-content {{
            background-color: #5D6ED4;
        }}
        .fish-container {{
            display: flex;
            justify-content: center;
            padding: 20px;
        }}
        .fish-gif {{
            width: 400px; /* Adjust the width as needed */
            height: auto;
            margin: 0 10px; /* Add some margin between each fish GIF */
        }}
        /* Adjusting the font size, weight, and color for all text */
        body, p, label, .stMarkdown {{
            font-size: 24px !important;
            font-weight: bold !important;
            color: #FF6EC7 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Define the API URLs
HEALTH_CHECK_API_URL = "https://fishapi-rhatlat23q-ew.a.run.app/analyze-image"  # Replace with the actual Health Check API URL
SPECIES_ID_API_URL = "https://fishapi-rhatlat23q-ew.a.run.app/id-species"      # Replace with the actual Species ID API URL

def predict_image(api_url, uploaded_files):
    results = []
    for uploaded_file in uploaded_files:
        file_contents = uploaded_file.read()
        files = {"file": ("image.jpg", file_contents, "image/jpeg")}
        response = requests.post(api_url, files=files)
        result = response.json()
        results.append(result)
    return results

def display_health_check_results(uploaded_files, results):
    for uploaded_file, result in zip(uploaded_files, results):
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        if "class_label" in result and "probability" in result:
            probability_percent = result["probability"] * 100
            formatted_probability = f"{probability_percent:.2f}%"
            st.write("Class Label:", result["class_label"])
            st.write("Probability:", formatted_probability)
        else:
            st.error("Error: Invalid response from the API")

def display_species_id_results(uploaded_files, results):
    for uploaded_file, result in zip(uploaded_files, results):
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        if "species_id" in result:
            st.write("Species:", result["species_id"])
        else:
            st.error("Error: Invalid response from the API")

def health_check_interface():
    st.subheader("Health Check")
    uploaded_files = st.file_uploader("Upload images for health check", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if uploaded_files:
        results = predict_image(HEALTH_CHECK_API_URL, uploaded_files)
        display_health_check_results(uploaded_files, results)

def species_id_interface():
    st.subheader("Species Identification")
    uploaded_files = st.file_uploader("Upload images for species identification", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if uploaded_files:
        results = predict_image(SPECIES_ID_API_URL, uploaded_files)
        display_species_id_results(uploaded_files, results)

def main():
    # Set the background at the start of the main function
    set_bg("background.webp")

    st.sidebar.title("Navigation")
    st.markdown("""
        <style>
        .sidebar .sidebar-content {{
            background-color: #5D6ED4;
        }}
        </style>
        """, unsafe_allow_html=True)

    # Load the fish GIF
    fish_gif = open("fish-spinning.gif", "rb").read()

    # Display the fish GIF multiple times in a horizontal row
    st.markdown('<p class="fish-container">' + ' '.join([f'<img class="fish-gif" src="data:image/gif;base64,{base64.b64encode(fish_gif).decode()}" alt="Fish GIF">' for _ in range(5)]) + '</p>', unsafe_allow_html=True)

    app_mode = st.sidebar.selectbox("Choose the app mode", ["Home Screen", "Health Check", "Species ID"])

    st.title("Fish Image Analyzer")
    if app_mode == "Home Screen":
        st.markdown("Welcome to the Fish Image Analyzer! Choose a mode from the sidebar.", unsafe_allow_html=True)
    elif app_mode == "Health Check":
        health_check_interface()
    elif app_mode == "Species ID":
        species_id_interface()

if __name__ == "__main__":
    main()
