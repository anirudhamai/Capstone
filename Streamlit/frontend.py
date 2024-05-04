# app.py (frontend)

import streamlit as st
import requests
from flask import redirect
import webbrowser


headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
SigninSection = st.container()
logOutSection = st.container()


if 'sign_up' not in st.session_state:
    st.session_state['sign_up']= False

if 'token' not in st.session_state:
    st.session_state['token']= "\0"


# Define the base URL of the backend
BASE_URL = 'http://localhost:5000'

# Define a function to handle user signup
def signup():
    with SigninSection:
        st.subheader("Sign Up")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        ph_no = st.text_input("Phone number")
        if st.button("Sign Up"):
            response = requests.post(f'{BASE_URL}/signup', json={'username': username, 'password': password,'phone_number':ph_no})
            if response.status_code == 201:
                st.success("Sign up successful! Please login.")
            else:
                st.error("Sign up failed. Please try again.")
        
        if st.button('Log_in'):
            st.session_state['sign_up'] = False


# Define a function to handle user login
def login():
    with loginSection:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login",key="l"):
            response = requests.post(f'{BASE_URL}/login', json={'username': username, 'password': password})
            if response.status_code == 200:
                # Save user token in session or local storage for future requests
                token = response.json()['token']
                st.success("Login successful!")
                # Redirect to homepage or other authenticated routes
                st.session_state['loggedIn'] = True
                st.session_state['token']=token
                # homepage(token)
            else:
                st.session_state['loggedIn'] = False
                st.error("Invalid username or password")
        if st.button('Sign_up'):
            st.session_state['sign_up'] = True
        



# Define the homepage after successful login
def homepage(token):
    with mainSection:
        st.empty()
        st.title("Home Security System - Homepage")

         # Add navigation
        menu = ["Upload Homeowner Data", "Watch Videos", "CCTV Feed Control","Log Out"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Upload Homeowner Data":
            upload_photos(token)
        elif choice == "Watch Videos":
            watch_videos()
        elif choice == "CCTV Feed Control":
            open_image()
        elif choice == "Log Out":
            show_logout_page()

# Define a function to upload homeowner photos
def upload_photos(token):
    st.subheader("Upload Homeowner's Photos")
    homeowner_name = st.text_input("Homeowner Name")
    uploaded_file = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Include token in the header for authentication
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(f'{BASE_URL}/upload', files={'file': uploaded_file}, data={'homeowner_name': homeowner_name}, headers=headers)
        if response.status_code == 201:
            st.success("Photo uploaded successfully!")
        else:
            st.error("Failed to upload photo. Please try again.")


# Define function to watch videos
def watch_videos():
    st.subheader("Watch Videos")
    video_path = r"C:\Users\91827\Desktop\Capstone\object_tracking_2.avi"
    st.video(video_path)

# Define function to open image
def open_image():
    # st.subheader("Open Image")
    st.subheader("Enable transfer of cctv footage")
    option = st.radio("Click yes to enable transfer of cctv footage", ("No", "Yes"))
    if option == "Yes":
        response = requests.get(f'{BASE_URL}/upload_video')
        if response.status_code == 201:
            st.success("Video sending successfully!")
    # Add functionality to open image here

def show_logout_page():
    loginSection.empty();
    with logOutSection:
        st.button ("Log Out", key="logout", on_click=LoggedOut_Clicked)

def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
# Define the main function to run the web application


    

def main():
    with headerSection:
        st.title("Home Security System")
        if 'loggedIn' not in st.session_state and st.session_state['sign_up']==False:
            st.session_state['loggedIn'] = False
            login()
        elif st.session_state['sign_up']:
            signup()
        elif st.session_state['loggedIn']:
            homepage(st.session_state['token'])
        else:
            if st.session_state['loggedIn']:
                loginSection.empty()
                show_logout_page()
            else:
                login()
        


if __name__ == "__main__":
    main()
