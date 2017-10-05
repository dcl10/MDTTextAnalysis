from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

def remove_stop_words(text):
    sw = list(stopwords.words("english"))
    sw.extend([".", ",", "?"])
    stopped = word_tokenize(text)
    for i in stopped:
        if i in sw: stopped.remove(i)
    return [str.join(" ", (i for i in stopped))]


def get_sentences(text):
    sentences = sent_tokenize(text)
    return sentences
