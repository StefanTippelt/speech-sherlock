import pandas as pd
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize


def tokenize(speech_content):
    if speech_content:
        return word_tokenize(speech_content)


def preprocess_words(words, stop_words):
    cleaned_words = []
    if words:
        for word in words:
            if word not in stop_words and word.isalpha():
                cleaned_words.append(word.lower())
        return cleaned_words


def get_word_counts(words, stop_words):
    cleaned_words = preprocess_words(words=words, stop_words=stop_words)
    word_counts = pd.Series(FreqDist(cleaned_words)).sort_values(
        ascending=False
    )
    return word_counts
