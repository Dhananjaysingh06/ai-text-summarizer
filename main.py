import nltk

# Download required resources (including the missing one)
nltk.download('punkt')
nltk.download('punkt_tab')   # 🔥 THIS fixes your error
nltk.download('stopwords')

import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict

# Page config (⚠️ must be first Streamlit command)
st.set_page_config(page_title="AI Text Summarizer", page_icon="📝", layout="centered")

# UI Styling
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("📝 AI Text Summarizer")
st.markdown("Paste your long text below and choose summary length.")

# Text input
text = st.text_area("Enter your text here:", height=250)

# Slider
summary_percent = st.slider("Select Summary Length (%)", 10, 90, 50)

# Button
if st.button("Generate Summary"):

    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        # Tokenization
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())

        # Stopwords
        stop_words = set(stopwords.words("english"))
        filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

        # Word frequency
        freq = defaultdict(int)
        for word in filtered_words:
            freq[word] += 1

        # Sentence scoring
        sentence_scores = defaultdict(int)
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in freq:
                    sentence_scores[sentence] += freq[word]

        # Number of sentences in summary
        num_sentences = max(1, int(len(sentences) * summary_percent / 100))

        # Get top sentences
        summary_sentences = sorted(
            sentence_scores, key=sentence_scores.get, reverse=True
        )[:num_sentences]

        # 🔥 Maintain original order (important improvement)
        summary_sentences = sorted(summary_sentences, key=lambda s: sentences.index(s))

        # Output
        st.subheader("📌 Summary:")
        for sentence in summary_sentences:
            st.write(sentence)

        st.success(f"Summary generated with {summary_percent}% length.")
