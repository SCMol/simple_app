import streamlit as st
import requests

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
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose the app mode", ["Home Screen", "Health Check", "Species ID"])

    st.title("Fish Image Analyzer")
    if app_mode == "Home Screen":
        st.markdown("Welcome to the Fish Image Analyzer! Choose a mode from the sidebar.")
    elif app_mode == "Health Check":
        health_check_interface()
    elif app_mode == "Species ID":
        species_id_interface()

if __name__ == "__main__":
    main()
