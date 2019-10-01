import pandas as pd
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


class TextInvestigate:
    def __init__(self, speech_content):
        self.speech_content = speech_content
        self.tokenized_words = self.tokenize()
        self.stop_words = set(stopwords.words("english"))
        self.cleaned_words = self.preprocess_words()

    def tokenize(self):
        """Tokenize words from `speech_content`."""
        if self.speech_content:
            self.tokenized_words = word_tokenize(self.speech_content)
            return self.tokenized_words

    def preprocess_words(self):
        """
        Preprocess `tokenized_words` by removing stop words and numerical 
        values.
        """
        self.cleaned_words = []
        if self.tokenized_words and len(self.tokenized_words) > 0:
            for word in self.tokenized_words:
                if word not in self.stop_words and word.isalpha():
                    self.cleaned_words.append(word.lower())
            return self.cleaned_words

    def get_raw_word_count(self):
        """Count words in `tokenized_words`."""
        self.raw_word_count = len(self.tokenized_words)
        return self.raw_word_count

    def get_cleaned_word_counts(self):
        """Count words in `cleaned_word_counts` after preprocessing."""
        self.cleaned_word_counts = pd.Series(
            FreqDist(self.cleaned_words)
        ).sort_values(ascending=False)
        return self.cleaned_word_counts
