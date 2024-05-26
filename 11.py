import nltk
from nltk.tokenize import word_tokenize

def determine_orientedness(sentence):
    # Tokenisation de la phrase
    tokens = word_tokenize(sentence)
    
    # Tagging des parties du discours avec NLTK
    tagged_words = nltk.pos_tag(tokens)
    
    # Compte les occurrences de noms (noms communs) et d'adjectifs (qui peuvent être utilisés pour décrire des concepts)
    noun_count = 0
    adj_count = 0
    
    for word, pos in tagged_words:
        if pos.startswith('CC'):  # thinking
            noun_count += 1
        elif pos.startswith('RB'):  # feeling
            adj_count += 1
    
    # Détermine l'orientation en fonction du nombre de noms et d'adjectifs
    if adj_count > noun_count:
        return "feeling"
    elif adj_count < noun_count:
        return "thinking"
    else:
        return "neutre"

# Exemple de phrases
phrases = [
    "La beauté de la nature est indéniable.",
    "The beauty of nature is undeniable.",
    "Les arbres dans le parc sont majestueux.",
    "The trees in the park are majestic.",
    "L'amour est un concept universel.",
    "Love is a universal concept.",
    "La science moderne a révolutionné notre compréhension du monde.",
    "Modern science has revolutionized our understanding of the world.",
    "j'ai bien aimé ce film"
]

# Détermine l'orientation de chaque phrase
for phrase in phrases:
    orientation = determine_orientedness(phrase)
    print(f"La phrase '{phrase}' est {orientation}.")