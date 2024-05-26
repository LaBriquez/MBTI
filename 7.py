import csv

import spacy
from textblob import TextBlob

nlp = spacy.load("fr_core_news_lg")


def analyze_sentiment_and_logic(sentence):
    analysis = TextBlob(sentence)

    doc = nlp(sentence)

    return {"tokens": [(token.pos_, token.dep_, token) for token in doc],
            "polarity": analysis.polarity,
            "subjectivity": analysis.subjectivity,
            "sentiment": doc.sentiment}


for line, user in csv.reader(open('values.csv'), delimiter=";"):
    analyse = analyze_sentiment_and_logic(line)

    print(analyse["sentiment"])