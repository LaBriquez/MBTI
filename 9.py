from textblob import TextBlob

def determine_orientedness(sentence):
    # Analyse la phrase avec TextBlob
    blob = TextBlob(sentence)
    
    # Compte les occurrences de noms (noms communs) et d'adjectifs (qui peuvent être utilisés pour décrire des concepts)
    noun_count = 0
    adj_count = 0
    
    for word, pos in blob.tags:
        if pos.startswith('NN'):  # Si le mot est un nom commun
            noun_count += 1
        elif pos.startswith('JJ'):  # Si le mot est un adjectif
            adj_count += 1
    
    # Détermine l'orientation en fonction du nombre de noms et d'adjectifs
    if adj_count > noun_count:
        return "orientée vers des concepts abstraits"
    elif adj_count < noun_count:
        return "orientée vers des faits concrets"
    else:
        return "neutre"

# Exemple de phrases
phrases = [
    "La beauté de la nature est indéniable.",
    "Les arbres dans le parc sont majestueux.",
    "L'amour est un concept universel.",
    "La science moderne a révolutionné notre compréhension du monde."
]

# Détermine l'orientation de chaque phrase
for phrase in phrases:
    orientation = determine_orientedness(phrase)
    print(f"La phrase '{phrase}' est {orientation}.")