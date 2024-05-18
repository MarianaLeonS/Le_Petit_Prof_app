import streamlit as st
from PIL import Image
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(jpg_file):
    bin_str = get_base64_of_bin_file(jpg_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/jpg;base64,%s");
        background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

def app():
    # Set the background image
    set_background('/workspaces/codespaces-blank/pages/wallpaper.jpg')

    # Include Google Font - Amatic SC
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Amatic+SC:wght@700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    # Add the header with the title and image
    image_path = "/workspaces/codespaces-blank/pages/lepetitprince.jpg"
    image_base64 = get_base64_image(image_path)
    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="data:image/jpg;base64,{image_base64}" alt="Le Petit Prince" style="height: 50px; margin-right: 10px;">
            <h1 style="font-family: 'Amatic SC'; font-weight: bold;">Le Petit Prof</h1>
        </div>
        """, unsafe_allow_html=True)

    # Welcoming message
    st.markdown("""
        <style>
        .welcome-message h2, .welcome-message p {
            color: #01793f;  /* Replace with your desired color */
            text-align: left;
        }
        </style>
        <div class="welcome-message">
            <h2>Bienvenue!</h2>
            <p>Welcome to Le Petit Prof, your friendly French learning companion!</p>
        </div>
    """, unsafe_allow_html=True)

    # List of contents with short descriptions
    st.markdown("""
        <h3 style='color: var(--secondary-color);'>Contents</h3>
        <ul>
            <li><b>Read:</b> Practice reading French sentences rating their difficulty.</li>
            <li><b>Write:</b> Compose sentences and I will rate your skills.</li>
            <li><b>Progress:</b> Track your progress over time.</li>
        </ul>
    """, unsafe_allow_html=True)

    st.header("Have fun by learning!")

    # Footer with copyright information and creators' names
    st.markdown("""
        <hr>
        <footer style='text-align: center; color: var(--text-color);'>
        &copy; 2024 Le Petit Prof. Created by Mariana Leon and Camille Vermenouze.
        </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
