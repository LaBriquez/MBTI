import spacy

# Charger le modèle de langue française de spaCy
nlp = spacy.load("fr_core_news_lg")

# Phrase d'exemple
phrase = "Le chat noir dort paisiblement sur le tapis."

# Traitement de la phrase avec spaCy
doc = nlp(phrase)

# Liste des verbes dans la phrase avec leur lemmatisation et leur analyse sémantique
verbes_semantique = []

for token in doc:
    if token.pos_ == 'VERB':
        verbes_semantique.append({
            'verbe': token.text,
            'lemme': token.lemma_,
            'analyse_semantique': token.vector  # Vecteur de représentation sémantique du verbe
        })

# Affichage des résultats
for verbe in verbes_semantique:
    print(f"Verbe: {verbe['verbe']}, Lemme: {verbe['lemme']}, Analyse sémantique: {verbe['analyse_semantique']}")