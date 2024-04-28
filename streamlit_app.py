# app.py

import streamlit as st
from PIL import Image
from datetime import datetime
import os

# Define a function to handle user signup
def signup():
    st.subheader("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        # Save user data (for demonstration purposes)
        with open("user_data.txt", "a") as file:
            file.write(f"{username},{password}\n")
        st.success("Sign up successful!")

# Define a function to handle user login
def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Check if user exists (for demonstration purposes)
        with open("user_data.txt", "r") as file:
            for line in file:
                stored_username, stored_password = line.strip().split(",")
                if username == stored_username and password == stored_password:
                    st.success("Login successful!")
                    return
        st.error("Invalid username or password")

# Define a function to upload homeowner photos
def upload_photos():
    st.subheader("Upload Homeowner Photos")
    homeowner_name = st.text_input("Homeowner Name")
    uploaded_file = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Save uploaded photo to a directory (for demonstration purposes)
        image = Image.open(uploaded_file)
        image_path = f"homeowner_photos/{homeowner_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        image.save(image_path)
        st.success("Photo uploaded successfully!")
        st.image(image, caption="Uploaded Photo", use_column_width=True)

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
