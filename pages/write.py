import streamlit as st
from transformers import CamembertForSequenceClassification, CamembertTokenizer
import torch
from spellchecker import SpellChecker
import pandas as pd
import random
import base64
import string
from datetime import datetime

# Set the page configuration
st.set_page_config(page_title="Le Petit Prof")

# Load the camemBERT model and tokenizer with exception handling
try:
    tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
    model = CamembertForSequenceClassification.from_pretrained("/workspaces/codespaces-blank/pages/camembert-model")  # Ensure your model is fine-tuned
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Initialize spell checker
spell = SpellChecker(language='fr')

# Difficulty categories
difficulty_levels = ["A1", "A2", "B1", "B2", "C1", "C2"]

# List of common French contractions
common_contractions = [
    "l'", "c'", "j'", "m'", "n'", "s'", "t'", "qu'", "d'", "s'être", "m'être", "t'être", "n'être", "qu'être",
    "l'un", "l'une", "l'homme", "l'enfant", "l'hôtel", "l'histoire", "c'est", "c'était", "c'est-à-dire", 
    "c'était", "c'étions", "c'étiez", "c'étaient", "d'abord", "d'accord", "d'ailleurs", "d'autres", 
    "d'autre part", "j'ai", "j'aurais", "j'aurais dû", "j'avais", "j'avais eu", "j'avais fait", "j'avais été", 
    "j'étais", "je n'ai", "j'y", "m'aimait", "m'appeler", "m'avertir", "m'appelle", "m'appelais", "m'appelait", 
    "m'appellera", "m'appellerait", "n'avons", "n'ai", "n'aie", "n'aies", "n'avait", "n'avions", "n'avez", 
    "n'avaient", "n'étions", "n'êtes", "n'étaient", "n'est", "n'êtes", "n'était", "n'aurons", "n'aurez", 
    "n'auriez", "n'auraient", "n'aurons pas", "n'auriez pas", "n'auraient pas", "n'auront pas", "qu'il", 
    "qu'elle", "qu'ils", "qu'elles", "qu'il y a", "qu'il y avait", "qu'il est", "qu'il était", "qu'il sera", 
    "qu'elle soit", "qu'elles soient", "qu'ils soient", "qu'elles aient", "qu'ils aient", "qu'il fasse", 
    "qu'il faille", "qu'ils fassent", "qu'elles fassent", "qu'on", "qu'on a", "qu'on avait", "qu'on soit", 
    "qu'on fût", "qu'on eût", "qu'on ait", "qu'on eut", "qu'on fit", "qu'on fasse", "qu'on faille", 
    "qu'on fallût", "qu'on pût", "qu'on dû", "qu'on puisse", "qu'on pût", "qu'on voulût", "qu'on sache", 
    "qu'on sut", "qu'on crût", "qu'on prît", "qu'on vît", "qu'on mît", "qu'on pût"
]

def classify_sentence(sentence):
    inputs = tokenizer(sentence, return_tensors="pt")
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=1)
    return difficulty_levels[predictions.item()]

def check_spelling(sentence):
    words = sentence.split()
    cleaned_words = [word.strip(string.punctuation) for word in words]  # Strip punctuation from words
    misspelled = [word for word in cleaned_words if word.lower() not in common_contractions and word.lower() not in spell]
    return len(misspelled) > 0, misspelled

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

def load_new_sentence(pp):
    random_sentence = random.choice(pp['sentence'].tolist())
    longest_word = max(random_sentence.split(), key=len)
    return random_sentence, longest_word

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
            Bonjour! Ready for a writting challenge?
        </div>
        """, unsafe_allow_html=True)

    st.header("✍️ Writing section")
    st.write("🌟Welcome. Here you can practice you writing skills. I will give you a word taken from a quote of the book The Little Prince by Antoine de Saint-Exupéry (...obviously 😎) and will challenge you to write the most complex and advanced sentence that comes to your mind by using thet word.")
    st.write("🌟Then I will read it and tell you the difficulty level of your sentence.")
    st.write("🌟You can skip to a new quote if nothing comes up to you mind and click new sentence if you want to keep playing, all your sentences will be stored in a dictionary for you to track your progress! How cool is that? ")

    # Initialize session state variables
    if "started" not in st.session_state:
        st.session_state.started = False
    if "pp" not in st.session_state:
        st.session_state.pp = pd.read_csv("/workspaces/codespaces-blank/pages/pp.csv")
    if "user_data" not in st.session_state:
        st.session_state.user_data = pd.DataFrame(columns=["Date", "Word", "Sentence", "Difficulty", "Spelling check"])
    if "random_sentence" not in st.session_state or "longest_word" not in st.session_state:
        st.session_state.random_sentence, st.session_state.longest_word = load_new_sentence(st.session_state.pp)

    if st.button("Start"):
        st.session_state.started = True

    if st.session_state.started:
        st.markdown(
            f"""
            <div style="margin-top: 1cm; margin-bottom: 1cm;">
                🌟Quote:
            </div>
            <div style="font-size: 20px; font-style: italic;">
                "{st.session_state.random_sentence}"
            </div>
            <div style="margin-top: 1cm; margin-bottom: 1cm;">
                🌟Your turn: 
                <span style="font-size: 20px; font-style: italic;">'{st.session_state.longest_word}'</span>. 
                Then click submit and I will tell you what French level I think you have.
            </div>
            """, unsafe_allow_html=True)

        user_sentence = st.text_input("Enter a French sentence:")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Submit"):
                if user_sentence:
                    # Check for spelling mistakes
                    has_misspelling, misspelled_words = check_spelling(user_sentence)
                    
                    # Classify the sentence
                    difficulty = classify_sentence(user_sentence)
                    
                    # Adjust difficulty if there are misspellings
                    if has_misspelling:
                        misspelled_words_str = ', '.join(misspelled_words)
                        spelling_check = f"Mistakes: {misspelled_words_str}"
                        st.warning(f"You might need to check your spelling; here is a suggested tool to do so! [Reverso](https://www.reverso.net/text-translation)")
                        if difficulty not in ["A1", "A2", "B1"]:
                            difficulty = "B1"
                    else:
                        spelling_check = "This seems correct"
                    
                    # Store the result with a timestamp
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    new_data = {"Date": timestamp, "Word": st.session_state.longest_word, "Sentence": user_sentence, "Difficulty": difficulty, "Spelling check": spelling_check}
                    st.session_state.user_data = pd.concat([st.session_state.user_data, pd.DataFrame([new_data])], ignore_index=True)
                    
                    # Display the result
                    st.write(f"The difficulty of the submitted sentence is: {difficulty}")

        with col2:
            if st.button("New Sentence"):
                st.session_state.random_sentence, st.session_state.longest_word = load_new_sentence(st.session_state.pp)
                st.experimental_rerun()

        with col3:
            if st.button("Skip"):
                st.session_state.random_sentence, st.session_state.longest_word = load_new_sentence(st.session_state.pp)
                st.experimental_rerun()

        # Display the stored user data
        if not st.session_state.user_data.empty:
            st.write("## Submitted Sentences and their Difficulty Levels")
            st.table(st.session_state.user_data)

        # Button to clear data
        if st.button("Clear Data"):
            st.session_state.user_data = pd.DataFrame(columns=["Date", "Word", "Sentence", "Difficulty", "Spelling check"])
            st.experimental_rerun()
        
        # Button to export data
        if st.button("Export your results"):
            if not st.session_state.user_data.empty:
                user_df = st.session_state.user_data
                user_df.to_csv("user_results.csv", index=False)
                st.success("Results exported successfully!")

if __name__ == "__main__":
    app()
