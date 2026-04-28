import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict

# Input text
text = input("Paste your long text:\n")

# Sentence tokenization
sentences = sent_tokenize(text)

# Word tokenization
words = word_tokenize(text.lower())

# Remove stopwords
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

# Select top 3 sentences
summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:3]

print("\n--- Summary ---")
for sentence in summary_sentences:
    print(sentence)
