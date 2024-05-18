import streamlit as st
import pandas as pd
import base64
import plotly.express as px

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

def app():
    # Add the header with the title and image
    image_path = "/workspaces/codespaces-blank/pages/lepetitprince.jpg"
    image_base64 = get_base64_image(image_path)

    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Amatic+SC:wght@700&display=swap" rel="stylesheet">
        <style>
        .custom-font {
            font-family: 'Amatic SC', cursive;
        }
        </style>
    """, unsafe_allow_html=True)

    # Add the header with the title and image
    image_path = "/workspaces/codespaces-blank/pages/lepetitprince.jpg"
    image_base64 = get_base64_image(image_path)
    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="data:image/jpg;base64,{image_base64}" alt="Le Petit Prince" style="height: 50px; margin-right: 10px;">
            <h1 class="custom-font" style="font-weight: bold;">Le Petit Prof</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        """
        <div style="font-size: 30px;">
            “The only guarantee for failure is to stop trying... surprisingly grown-ups can also say things that make sense”
        </div>
        """, unsafe_allow_html=True)

    st.header("🎖️ Your Progress")
    st.write("Here you can track how much you have learnt and re-read your favourite quotes from Le Petit Prince.")

    # Display detailed results from reading
    if "all_rated_sentences" in st.session_state and not st.session_state.all_rated_sentences.empty:
        st.subheader("📚The sentences you have read.")
        st.write("✅Here is the history of all your rated sentences:")
        st.dataframe(st.session_state.all_rated_sentences)

        # Plot the estimated level over time
        if "user_attempts" in st.session_state and not st.session_state.user_attempts.empty:
            st.subheader("📚 Estimated Reading Level per Attempt")
            fig_reading = px.line(
                st.session_state.user_attempts,
                x='Attempt',
                y='Estimated level',
                title='Estimated Reading Level Over Time'
            )
            st.plotly_chart(fig_reading)

    else:
        st.write("No rated sentences found.")

    # Display comprehension levels
    if "user_attempts" in st.session_state and not st.session_state.user_attempts.empty:
        st.subheader("📚Comprehension Levels")
        st.write("✅Here is the history of all your comprehension levels:")
        st.dataframe(st.session_state.user_attempts)

    else:
        st.write("No comprehension levels found.")

    # Display results from writing
    if "user_data" in st.session_state and not st.session_state.user_data.empty:
        st.subheader("✍️Writing Results")
        st.write("✅Here is the history of all your writing attempts:")
        st.dataframe(st.session_state.user_data)

        # Plot the difficulty over time for writing results
        st.subheader("✍️Writing Difficulty Over Time")
        fig_writing = px.line(
            st.session_state.user_data,
            x='Date',
            y='Difficulty',
            title='Writing Difficulty Over Time'
        )
        st.plotly_chart(fig_writing)

    else:
        st.write("No writing results found.")

# Run the progress page
if __name__ == "__main__":
    app()
