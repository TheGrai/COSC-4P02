from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

sentence = "As we all know, Mr. Steve is stupidly fun."
stop_words = set(stopwords.words("english"))
stemmer = SnowballStemmer("english")

# tokenize words
words = word_tokenize(sentence)

# filter words
filtered_sentence = []
for w in words:
    # filter stop words
    if w not in stop_words:
        # stem words
        w = stemmer.stem(w)
        filtered_sentence.append(w)

print(filtered_sentence)
