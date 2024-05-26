from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer
import spacy
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer

nlp = spacy.load("fr_core_news_lg")
SIA = SentimentIntensityAnalyzer()


def determine(sentence: str):
    doc = nlp(sentence)

    blob = TextBlob(sentence, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())

    subjectivity = blob.subjectivity

    noun_count = 0
    adj_count = 0

    sentiment_sia = SIA.polarity_scores(sentence)

    for token in doc:
        if token.pos_ in ['ADJ']:
            adj_count += 1
        elif token.pos_ in ['NOUN', 'SCONJ']:
            noun_count += 1

    feeling = adj_count + sentiment_sia["neg"] + sentiment_sia["pos"] + subjectivity
    thinking = noun_count + sentiment_sia["neu"]

    return "F" if feeling > thinking else "T"


phrases = [
    "non, c'est impossible",
    "les bons soldats obeissent aux ordres",
    "fait ou ne le fait pas, il n'y a pas d'éssai",
    "aucune limite à mon pouvoir",
    "sois tu es avec moi, sois tu est contre moi",
    "tu était l'élu c'était toi!",
    "je te hais!"
]

for phrase in phrases:
    SentimentIntensityAnalyzer()
    sentiment_score = determine(phrase)
    print(f"'{phrase}' : {sentiment_score}")