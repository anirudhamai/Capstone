# app.py (frontend)

import streamlit as st
import requests

# Define the base URL of the backend
BASE_URL = 'http://localhost:5000'

# Define a function to handle user signup
def signup():
    st.subheader("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        response = requests.post(f'{BASE_URL}/signup', json={'username': username, 'password': password})
        if response.status_code == 201:
            st.success("Sign up successful!")
        else:
            st.error("Sign up failed. Please try again.")

# Define a function to handle user login
def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = requests.post(f'{BASE_URL}/login', json={'username': username, 'password': password})
        if response.status_code == 200:
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

# Define a function to upload homeowner photos
def upload_photos():
    st.subheader("Upload Homeowner Photos")
    homeowner_name = st.text_input("Homeowner Name")
    uploaded_file = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        response = requests.post(f'{BASE_URL}/upload', files={'file': uploaded_file}, data={'homeowner_name': homeowner_name})
        if response.status_code == 201:
            st.success("Photo uploaded successfully!")
        else:
            st.error("Failed to upload photo. Please try again.")

# Define the main function to run the web application
def main():
    st.title("Home Security System")

    # Add navigation
    menu = ["Login", "Sign Up", "Upload Homeowner Photos"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        login()
    elif choice == "Sign Up":
        signup()
    elif choice == "Upload Homeowner Photos":
        upload_photos()

if __name__ == "__main__":
    main()
