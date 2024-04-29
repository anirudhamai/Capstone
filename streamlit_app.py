import streamlit as st

def login():
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        # Here you would add authentication logic
        if username == 'user' and password == 'password':
            st.success('Login successful!')
            st.session_state['authenticated'] = True
        else:
            st.error('Invalid username or password')

def signup():
    st.title('Sign Up')
    st.write('Sign up functionality goes here.')

def home():
    st.title('Home')
    st.write('Welcome to the home page. Choose an option from below:')
    if st.button('Upload Home Owner\'s Data'):
        st.write('Functionality to upload home owner\'s data goes here.')
    if st.button('Watch Videos'):
        st.write('Functionality to watch videos goes here.')
    if st.button('Open an Image'):
        st.write('Functionality to open an image goes here.')

def main():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        login()
        st.write('[Sign Up](signup)')
    else:
        home()

if __name__ == '__main__':
    main()
