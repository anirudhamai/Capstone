import streamlit as st

def page1():
    st.title('Page 1')
    st.write('Click the link below to navigate to Page 2:')
    if st.sidebar.write('[Go to Page 2](page2)'):
        pass

def page2():
    st.title('Page 2')
    st.write('Welcome to Page 2')

def main():
    page = st.session_state.get('page', 'page1')

    if page == 'page1':
        page1()
    elif page == 'page2':
        page2()

if __name__ == '__main__':
    main()
