import streamlit as st
import pandas as pd
import base64
from datetime import datetime

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def get_labelled_sentences(df, existing_labels=None):
    if existing_labels is None:
        existing_labels = []
    labelled_book = pd.DataFrame(columns=['sentence', 'difficulty'])
    while len(labelled_book['difficulty'].unique()) < 6:
        sample = df[~df['sentence'].isin(existing_labels)].sample(6)
        temp_df = pd.DataFrame({'sentence': sample['sentence'], 'difficulty': sample['difficulty']})
        labelled_book = pd.concat([labelled_book, temp_df]).drop_duplicates().reset_index(drop=True)
    return labelled_book

def reset_all_sliders(reset_iteration):
    st.session_state.reset_iteration = reset_iteration
    for i in range(6):
        st.session_state[f"rating_{i}_{reset_iteration}"] = "Too easy"

def app():
    # Load the full dataframe (book) with difficulty labels
    book = pd.read_csv('/workspaces/codespaces-blank/pages/pp.csv')

    # Define difficulty levels
    difficulty_levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']

    # Initialize session state variables
    if "user_attempts" not in st.session_state:
        st.session_state.user_attempts = pd.DataFrame(columns=['Attempt', 'Result', 'Estimated level', 'Timestamp'])
    if "all_rated_sentences" not in st.session_state:
        st.session_state.all_rated_sentences = pd.DataFrame(columns=['sentence', 'difficulty', 'Reply', 'Timestamp'])

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
            Bonjour! do you want to play a reading game?
        </div>
        """, unsafe_allow_html=True)

    st.header("📚Reading section")
    st.write("🌟Welcome. Here you can practice reading French sentences extracted from the book The Little Prince by Antoine de Saint-Exupéry and rating their difficulty.")   
    st.write("🌟Read the following sentences and drag the slider depending on how difficult it is for you to understand them. Then click submit and I will estimate what is your reading comprehension level. ")
    

    if st.button("Start"):
        st.session_state.started = True
        st.session_state.reset_iteration = st.session_state.get("reset_iteration", 0) + 1
        st.session_state.labelled_book = get_labelled_sentences(book)
        st.session_state.subset = pd.concat([st.session_state.labelled_book[st.session_state.labelled_book['difficulty'] == level].sample(1) for level in difficulty_levels]).reset_index(drop=True)
        st.session_state.subset['Reply'] = None
        reset_all_sliders(st.session_state.reset_iteration)

    if "started" in st.session_state:
        user_responses = []
        for i in range(6):
            st.text_area(
                f"🌟Sentence {i+1}", st.session_state.subset['sentence'][i], height=100, disabled=True, key=f"sentence_{i}_{st.session_state.reset_iteration}"
            )
            rating_key = f"rating_{i}_{st.session_state.reset_iteration}"
            rating = st.select_slider(
                f"Difficulty {i+1}",
                options=["Too easy", "Easy", "Right level", "A bit difficult", "Very difficult", "Impossible to understand"],
                key=rating_key,
                value=st.session_state.get(rating_key, "Too easy")
            )
            user_responses.append(rating)
            rating_map = {
                "Too easy": 5,
                "Easy": 4,
                "Right level": 3,
                "A bit difficult": 2,
                "Very difficult": 1,
                "Impossible to understand": 0
            }
            st.session_state.subset.at[i, 'Reply'] = rating_map[rating]

        if st.button("Submit"):
            updated_subset = pd.DataFrame(st.session_state.subset)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            updated_subset['Timestamp'] = timestamp

            # Append the new rated sentences to the cumulative dataframe
            st.session_state.all_rated_sentences = pd.concat([st.session_state.all_rated_sentences, updated_subset], ignore_index=True)

            comprehension_score = updated_subset['Reply'].sum()

            if 0 <= comprehension_score <= 4:
                level = "A1"
            elif 5 <= comprehension_score <= 9:
                level = "A2"
            elif 10 <= comprehension_score <= 14:
                level = "B1"
            elif 15 <= comprehension_score <= 20:
                level = "B2"
            elif 21 <= comprehension_score <= 25:
                level = "C1"
            elif 26 <= comprehension_score <= 30:
                level = "C2"

            st.write(updated_subset)
            st.write(f"✅Well done! Le Petit Prof estimates you have a French comprehension level of: {level}")
            st.header('If you want to try again go back to the top and click the Start button!')

            new_attempt = pd.DataFrame({
                'Attempt': [len(st.session_state.user_attempts) + 1],
                'Result': [comprehension_score],
                'Estimated level': [level],
                'Timestamp': [timestamp]
            })
            st.session_state.user_attempts = pd.concat([st.session_state.user_attempts, new_attempt], ignore_index=True)

            st.write(st.session_state.user_attempts)

        if st.button("Clear data"):
            st.session_state.clear()

        if st.button("Export your results"):
            csv = st.session_state.all_rated_sentences.to_csv(index=False)
            st.download_button(label="Download data as CSV", data=csv, file_name='results.csv', mime='text/csv')

        if book[~book['sentence'].isin(st.session_state.labelled_book['sentence'].tolist())].empty:
            st.write("Congratulations! You have now read the entire book Le Petit Prince by Saint Exupery! If you want to keep learning French you can clear the data and try again … OR … you can try another of your favourite books by subscribing to our Book Lovers group.")

    else:
        st.write("Click 'Start' to begin reading sentences.")

# Run the app
if __name__ == "__main__":
    app()
