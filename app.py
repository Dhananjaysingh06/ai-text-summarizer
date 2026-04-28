import nltk
nltk.download('punkt')
nltk.download('stopwords')
import streamlit as st
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


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict

st.set_page_config(page_title="AI Text Summarizer", page_icon="📝", layout="centered")

st.title("📝 AI Text Summarizer")
st.markdown("Paste your long text below and choose summary length.")

# Text input
text = st.text_area("Enter your text here:", height=250)

# Slider for summary percentage
summary_percent = st.slider("Select Summary Length (%)", 10, 90, 50)

if st.button("Generate Summary"):

    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())

        stop_words = set(stopwords.words("english"))
        filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

        freq = defaultdict(int)
        for word in filtered_words:
            freq[word] += 1

        sentence_scores = defaultdict(int)
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in freq:
                    sentence_scores[sentence] += freq[word]

        # Calculate number of sentences based on percentage
        num_sentences = max(1, int(len(sentences) * summary_percent / 100))

        summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]

        st.subheader("📌 Summary:")
        for sentence in summary_sentences:
            st.write(sentence)

        st.success(f"Summary generated with {summary_percent}% length.")
