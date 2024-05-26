import spacy
from flair.models import TextClassifier
from flair.data import Sentence


classifier = TextClassifier.load('sentiment-fr')

nlp = spacy.load("fr_core_news_lg")


def determine_orientedness(sentence: str):
    s = Sentence(sentence)
    classifier.predict(s)
    sentiment = s.labels[0]

    # Traite le texte avec le modèle de langue français de SpaCy
    doc = nlp(sentence)

    noun_count = 0
    adj_count = 0

    for token in doc:
        print(token.pos_, token)
        if token.pos_ == 'ADJ':
            adj_count += 1
        elif token.pos_ == 'NOUN':
            noun_count += 1

    return "sentimental" if adj_count > noun_count else "rationnel", sentiment.value, sentiment.score


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
    orientation = determine_orientedness(phrase)
    print(f"{phrase} : {orientation}.")