from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer
import spacy
import numpy as np
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer

nlp = spacy.load("fr_core_news_lg")
SIA = SentimentIntensityAnalyzer()

vect_sentiments = np.mean([nlp(verbe).vector for verbe in ["amour", "haine", "sentiments"]], axis=0)

vect_raisonement = np.mean([nlp(verbe).vector for verbe in ["raison", "concret"]], axis=0)


def determine(sentence: str):
    doc = nlp(sentence)

    blob = TextBlob(sentence, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())

    subjectivity = blob.subjectivity

    sentiment_sia = SIA.polarity_scores(sentence)

    print(sentiment_sia)

    feeling = abs(sentiment_sia["neg"]) + abs(sentiment_sia["pos"]) + subjectivity
    thinking = 0  # sentiment_sia["neu"]