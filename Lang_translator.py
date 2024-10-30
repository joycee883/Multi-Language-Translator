import streamlit as st
from mtranslate import translate
import pandas as pd
from gtts import gTTS

# Read the language dataset
df = pd.read_csv(r'C:\Users\91939\Desktop\AI&DS\Data science projects\LanguageTranslator\language.csv')
df.dropna(inplace=True)

# Extract language names and codes into lists
languages = df['name'].to_list()
language_list = tuple(languages)
language_codes = df['iso'].to_list()

# Create a dictionary to map language names to their corresponding ISO codes
language_dict = {languages[i]: language_codes[i] for i in range(len(language_codes))}

# Set up the Streamlit layout
st.title("Multi-Language Translation Application")
input_text = st.text_area("Enter Text for Translation:", height=100)

# Sidebar for language selection
selected_language = st.sidebar.radio('Select Target Language:', language_list)

# Define supported languages for speech synthesis
speech_languages = {
    "af": "Afrikaans",
    "ar": "Arabic",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "eo": "Esperanto",
    "es": "Spanish",
    "et": "Estonian",
    "fi": "Finnish",
    "fr": "French",
    "gu": "Gujarati",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "hy": "Armenian",
    "id": "Indonesian",
    "is": "Icelandic",
    "it": "Italian",
    "ja": "Japanese",
    "jw": "Javanese",
    "km": "Khmer",
    "kn": "Kannada",
    "ko": "Korean",
    "la": "Latin",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mr": "Marathi",
    "my": "Myanmar (Burmese)",
    "ne": "Nepali",
    "nl": "Dutch",
    "no": "Norwegian",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "si": "Sinhala",
    "sk": "Slovak",
    "sq": "Albanian",
    "sr": "Serbian",
    "su": "Sundanese",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Filipino",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "zh-CN": "Chinese"
}

# Create columns for the output display
col_translated, col_audio = st.columns([4, 3])

# Button for translation
if st.button("Translate"):
    if len(input_text) > 0:
        try:
            # Translate the input text
            translated_output = translate(input_text, language_dict[selected_language])
            
            with col_translated:
                # Display the translated text
                st.subheader("Translated Text:")
                st.text_area("", translated_output, height=200)

            # Generate and display audio if the selected language supports speech
            if selected_language in speech_languages.values():
                with col_audio:
                    st.subheader("Audio Playback:")
                    # Create audio file from translated text
                    audio_file = gTTS(text=translated_output, lang=language_dict[selected_language], slow=False)
                    audio_file.save("translated_audio.mp3")  # Save audio as mp3

                    # Read and play the audio file
                    audio_file_read = open('translated_audio.mp3', 'rb')
                    audio_bytes = audio_file_read.read()
                    st.audio(audio_bytes, format='audio/mp3')

        except Exception as e:
            # Handle errors and display messages
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter text to translate.")
