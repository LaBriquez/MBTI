import math

import discord
import spacy
from spacy.tokens import Doc
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer

nlp = spacy.load("fr_core_news_lg")
SIA = SentimentIntensityAnalyzer()

recherche_vector = np.mean([nlp(verbe).vector for verbe in
                            ["rechercher", "étudier", "envisager", "penser", "croire"]], axis=0)
action_vector = np.mean([nlp(verbe).vector for verbe in ["agir", "observer", "ressentir"]], axis=0)

vect_sentiments = np.mean([nlp(verbe).vector for verbe in ["amour", "haine", "sentiments"]], axis=0)
vect_raisonement = np.mean([nlp(verbe).vector for verbe in ["raison", "concret"]], axis=0)

mbti_values: dict[int, dict[str, float]] = {}


def get_doc(phrase: str):
    return nlp(phrase)


def get_blob(phrase: str):
    return TextBlob(phrase, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())


def get_sia(phrase: str):
    return SIA.polarity_scores(phrase)


def analize_NS(doc: Doc):
    verbes = [{
        'verbe': token.text,
        'lemme': token.lemma_,
        'analyse_semantique': token.vector  # Vecteur de représentation sémantique du verbe
    } for token in doc if token.pos_ == 'VERB']

    total_sensing = 0.0
    total_intuition = 0.0

    for verbe in verbes:
        divid_action = np.linalg.norm(verbe['analyse_semantique']) * np.linalg.norm(action_vector)
        divid_recherche = np.linalg.norm(verbe['analyse_semantique']) * np.linalg.norm(recherche_vector)

        action_similarity = np.dot(verbe['analyse_semantique'], action_vector) / divid_action \
            if divid_action != 0 else 0
        recherche_similarity = np.dot(verbe['analyse_semantique'], recherche_vector) / divid_recherche \
            if divid_recherche != 0 else 0

        print(f"Verbe: {verbe['verbe']}, Lemme: {verbe['lemme']}")
        print(f"Similarité avec 'action': {action_similarity}")
        print(f"Similarité avec 'recherche': {recherche_similarity}")

        total_sensing += action_similarity * 0.5 + 0.5
        total_intuition += recherche_similarity * 0.5 + 0.5

    return total_sensing, total_intuition


def analize_TF(doc: Doc, blob: TextBlob, sentiment_sia: dict[str, float]):
    subjectivity = blob.subjectivity

    print(sentiment_sia)

    feeling = sentiment_sia["neg"] * 0.5 + 0.5 + sentiment_sia["pos"] * 0.5 + 0.5 + subjectivity
    thinking = sentiment_sia["neu"] * 0.5 + 0.5

    if math.isnan(feeling):
        feeling = 0.0

    if math.isnan(thinking):
        thinking = 0.0

    print(f"feeling : {feeling}, thinking : {thinking}")

    verbes = [{'verbe': token.text, 'lemme': token.lemma_, 'analyse_semantique': token.vector}
              for token in doc if token.pos_ == 'VERB']

    for verbe in verbes:
        divid_sent = np.linalg.norm(verbe['analyse_semantique']) * np.linalg.norm(vect_sentiments)
        divid_rais = np.linalg.norm(verbe['analyse_semantique']) * np.linalg.norm(vect_raisonement)

        sentiments_similarity = np.dot(verbe['analyse_semantique'], vect_sentiments) / divid_sent \
            if divid_sent != 0 and not math.isnan(divid_sent) else 0
        raisonement_similarity = np.dot(verbe['analyse_semantique'], vect_raisonement) / divid_rais \
            if divid_rais != 0 and not math.isnan(divid_rais) else 0

        print(f"Verbe: {verbe['verbe']}, Lemme: {verbe['lemme']}")
        print(f"Similarité avec 'sentiments': {sentiments_similarity}")
        print(f"Similarité avec 'raisonement': {raisonement_similarity}")

        feeling += sentiments_similarity * 0.5 + 0.5
        thinking += raisonement_similarity * 0.5 + 0.5

    return feeling, thinking


force_side: dict[int, dict[str, float]] = {}


def analize_side_content(message: discord.message.Message, content: str):
    if message.author.id not in force_side.keys():
        force_side[message.author.id] = {'neg': 0.0,
                                         'neu': 0.0,
                                         'pos': 0.0,
                                         'compound': 0.0,
                                         'total': 0}

    mess_val = SIA.polarity_scores(content)

    force_side[message.author.id]['compound'] += mess_val['compound'] * 0.5 + 0.5

    force_side[message.author.id]['total'] += 1
