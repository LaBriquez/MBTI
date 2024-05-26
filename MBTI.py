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

self_referential_pronouns = {"je", "moi", "mon"}

recherche_vector = np.mean([nlp(verbe).vector for verbe in
                            ["réfléchir", "rechercher", "étudier", "envisager", "penser", "croire", "apprendre"]], axis=0)
action_vector = np.mean([nlp(verbe).vector for verbe in ["réfléchir", "observer", "récupérer"]], axis=0)

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

    total = total_sensing + total_intuition + 0.0000000001

    return total_sensing / total, total_intuition / total


def analize_TF(doc: Doc, blob: TextBlob, sentiment_sia: dict[str, float]):
    subjectivity = blob.subjectivity

    print(sentiment_sia)

    subj = sentiment_sia["neg"] * 0.5 + 0.5 + sentiment_sia["pos"] * 0.5 + 0.5 + subjectivity
    neut = sentiment_sia["neu"] * 0.5 + 0.5

    feeling = 0.0
    thinking = 0.0

    if math.isnan(subj):
        subj = 0.0

    if math.isnan(neut):
        neut = 0.0

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

    total = feeling + thinking + 0.0000000001

    return (feeling / total + subj) * 0.5, (thinking / total + neut) * 0.5


def ego_size(doc: Doc):
    ego_total = 0
    solo = 0

    for token in doc:
        if token.pos_ == "VERB":
            ego_total += 1
            print(f"person : {token.morph.get("Person")}, Number : {token.morph.get("Number")}")
            if token.morph.get("Person") == ["1"] and token.morph.get("Number") == ["Sing"]:
                solo += 1

    # self_words = [token.text for token in doc if token.text.lower() in self_referential_pronouns]
    prons = [token for token in doc if token.pos_ == "PRON"]
    self_words = [token for token in prons if token.text.lower() in self_referential_pronouns]

    return (solo / (ego_total + 0.0000000000000000001) + len(self_words) / (len(prons) + 0.0000000000000000001)) * 0.5


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
