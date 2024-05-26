from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer
import spacy
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer

nlp = spacy.load("fr_core_news_lg")
SIA = SentimentIntensityAnalyzer()


def determine(sentence: str):
    doc = nlp(sentence)

    sentiment = TextBlob(sentence, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer()).sentiment

    noun_count = 0
    adj_count = 0

    sentimentSIA = SIA.polarity_scores(sentence)

    for token in doc:
        if token.pos_ in ['ADJ', 'ADV']:
            adj_count += 1
        elif token.pos_ in ['NOUN', 'SCONJ']:
            noun_count += 1

    total_sent = abs(sentiment[0]) + abs(sentiment[1])

    feeling = adj_count + total_sent + sentimentSIA["neg"] + sentimentSIA["pos"]
    thinking = noun_count + sentimentSIA["neu"]

    return "F" if feeling > thinking else "T" if feeling < thinking else "mid"


phrases = [
    "non, c'est impossible",
    "les bons soldats obeissent aux ordres",
    "fait ou ne le fait pas, il n'y a pas d'éssai",
    "aucune limite à mon pouvoir",
    "sois tu es avec moi, sois tu est contre moi",
    "tu était l'élu c'était toi",
    "je te hais"
]

for phrase in phrases:
    SentimentIntensityAnalyzer()
    sentiment_score = determine(phrase)
    print(f"'{phrase}' : {sentiment_score}")