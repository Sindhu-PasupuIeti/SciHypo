import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from collections import Counter
from heapq import nlargest

nlp = spacy.load("en_core_web_sm")


def generate_summary(text, ratio=0.5):
    doc = nlp(text)
    tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]
    word_freq = Counter(tokens)
    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    sentence_scores = {}
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in word_freq.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_freq[word.text.lower()]
                else:
                    sentence_scores[sent] += word_freq[word.text.lower()]

    summarized_sentences = nlargest(int(len(sentence_scores) * ratio), sentence_scores, key=sentence_scores.get)
    summary = " ".join([sent.text for sent in summarized_sentences])

    return summary
