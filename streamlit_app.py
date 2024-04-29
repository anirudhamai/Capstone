import streamlit as st

# Define session_state variables
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

# Define the login page
def login_page():
    st.title('Login Page')
    st.write('This is the login page')
    if st.button('Go to Sign Up Page'):
        st.session_state['page'] = 'signup'

# Define the sign-up page
def signup_page():
    st.title('Sign Up Page')
    st.write('This is the sign-up page')
    if st.button('Go to Login Page'):
        st.session_state['page'] = 'login'

# Main function to switch between pages
def main():
    if st.session_state['page'] == 'login':
        login_page()
    elif st.session_state['page'] == 'signup':
        signup_page()

if __name__ == "__main__":
    main()
