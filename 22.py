import spacy
import numpy as np

# Charger le modèle de langue française de spaCy
nlp = spacy.load("fr_core_news_lg")

# Phrases d'exemple
phrases = ["On avancera ce soir au pire.", "ça te dérange si je t'attire dans un piège?", "tu sais on a kwa à manger?", "après c utilisé surtout avec des formulaires", "après justement quand je parle je suis très rarament subjectif"]

# Vecteur de représentation sémantique de l'action
action_vector = nlp("action").vector

# Vecteur de représentation sémantique de la recherche/analyse
recherche_vector = nlp("recherche").vector

for phrase in phrases:
    print(f"Analyse de la phrase : '{phrase}'")
    print("-------------------------------")
    
    # Traitement de la phrase avec spaCy
    doc = nlp(phrase)

    # Liste des verbes dans la phrase avec leur lemmatisation et leur analyse sémantique
    verbes = []

    for token in doc:
        if token.pos_ == 'VERB':
            verbes.append({
                'verbe': token.text,
                'lemme': token.lemma_,
                'analyse_semantique': token.vector  # Vecteur de représentation sémantique du verbe
            })

    # Comparaison des vecteurs des verbes avec les vecteurs d'action et de recherche
    for verbe in verbes:
        action_similarity = np.dot(verbe['analyse_semantique'], action_vector) / (np.linalg.norm(verbe['analyse_semantique']) * np.linalg.norm(action_vector))
        recherche_similarity = np.dot(verbe['analyse_semantique'], recherche_vector) / (np.linalg.norm(verbe['analyse_semantique']) * np.linalg.norm(recherche_vector))

        print(f"Verbe: {verbe['verbe']}, Lemme: {verbe['lemme']}")
        print(f"Similarité avec 'action': {action_similarity}")
        print(f"Similarité avec 'recherche': {recherche_similarity}")

        if action_similarity > recherche_similarity:
            print("S")
        else:
            print("N")
        print()
    print()