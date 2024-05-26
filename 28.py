import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

nlp = spacy.load("fr_core_news_sm")

def calculer_similarite_cosinus(message1, message2):
    doc1 = nlp(message1)
    doc2 = nlp(message2)
    vecteur1 = doc1.vector.reshape(1, -1)
    vecteur2 = doc2.vector.reshape(1, -1)
    similarite = cosine_similarity(vecteur1, vecteur2)
    return similarite[0][0]

def evaluer_cohérence_messages(messages):
    similarites = []
    for i in range(len(messages)):
        for j in range(i+1, len(messages)):
            similarite = calculer_similarite_cosinus(messages[i], messages[j])
            similarites.append(similarite)
    moyenne_similarites = np.mean(similarites)
    return moyenne_similarites

messages = [
    "Premier message.",
    "Deuxième message.",
    "Troisième message.",
    # Ajoutez d'autres messages ici...
]

coherence = evaluer_cohérence_messages(messages)
print("Cohérence moyenne entre les messages:", coherence)