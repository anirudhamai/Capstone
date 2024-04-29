# Define the homepage after successful login
def homepage(token):
    st.empty()
    st.title("Home Security System - Homepage")

    # Add navigation
    menu = ["Upload Homeowner Data", "Watch Videos", "Open Image"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Upload Homeowner Data":
        upload_photos(token)
    elif choice == "Watch Videos":
        watch_videos()
    elif choice == "Open Image":
        open_image()

# Modify the main function to pass the token to the homepage
def main():
    st.title("Home Security System")
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        login() 
    else:
        if st.session_state['loggedIn']:
            show_logout_page()    
            token = get_token()  # Retrieve the token from somewhere
            homepage(token)  # Pass the token to the homepage function
        else:
            login()
