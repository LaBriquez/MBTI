import spacy

# Charger le modèle de langue en français
nlp = spacy.load("fr_core_news_sm")

def detecter_nombre_sujets(message):
    # Traiter le message avec le modèle de langue SpaCy
    doc = nlp(message)
    
    # Créer un ensemble pour stocker les sujets uniques
    sujets = set()
    
    # Parcourir les tokens dans le document
    for token in doc:
        # Vérifier si le token est un sujet (nom, pronom, etc.)
        if token.pos_ in ["NOUN", "PROPN"]:
            # Ajouter le sujet à l'ensemble
            sujets.add(token.text.lower())  # Utiliser le texte en minuscules pour éviter les doublons
    
    # Retourner le nombre de sujets détectés
    for sujet in sujets:
      print(sujet)
    return len(sujets)

# Exemple d'utilisation
message = "Je suis allé à la plage avec mes amis. Nous avons nagé et joué au volley-ball."
nombre_sujets = detecter_nombre_sujets(message)
print("Nombre de sujets évoqués dans le message :", nombre_sujets)