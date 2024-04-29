# frontend.py

import streamlit as st
from streamlit.state.session_state import SessionState

# Define a function to handle the navigation to the new page
def open_new_page():
    st.write("This is the new page!")

# Define the main function to run the web application
def main():
    st.title("Navigation Example")

    # Check if the button to open the new page has been clicked
    session_state = SessionState.get(button_clicked=False)

    # Button to trigger the navigation to the new page
    if st.button("Open New Page"):
        session_state.button_clicked = True

    # Check if the button has been clicked
    if session_state.button_clicked:
        open_new_page()

if __name__ == "__main__":
    main()
