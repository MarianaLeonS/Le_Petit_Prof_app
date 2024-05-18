import streamlit as st
from pages import home, read, progress, write

PAGES = {
    "Home": home,
    "Read": read,
    "Write": write,
    "Progress": progress  
}

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.selectbox("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()

if __name__ == "__main__":
    main()
