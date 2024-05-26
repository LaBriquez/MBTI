import spacy

# Charger le modèle de langue SpaCy
nlp = spacy.load("fr_core_news_lg")

def trouver_arguments(phrase):
    # Analyse syntaxique de la phrase
    doc = nlp(phrase)
    
    # Liste pour stocker les mots qui pourraient être des arguments
    arguments = []
    
    # Parcourir chaque token dans la phrase
    for token in doc:
        # Vérifier si le token est un sujet, un objet ou un complément
        if token.dep_ in ["nsubj", "obj", "iobj", "obl"]:
            arguments.append(token.text)
    
    return arguments

# Exemple d'utilisation
phrase = "Les politiques environnementales devraient être renforcées pour protéger notre planète."
arguments_trouves = trouver_arguments(phrase)
print("Mots pouvant être des arguments :", arguments_trouves)