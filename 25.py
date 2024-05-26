    print(f"feeling : {feeling}, thinking : {thinking}")

    verbes = [{'verbe': token.text, 'lemme': token.lemma_, 'analyse_semantique': token.vector}
              for token in doc if token.pos_ == 'VERB']

    for verbe in verbes:
        sentiments_similarity = np.dot(verbe['analyse_semantique'], vect_sentiments) / (
                np.linalg.norm(verbe['analyse_semantique']) * np.linalg.norm(vect_sentiments))

        raisonement_similarity = np.dot(verbe['analyse_semantique'], vect_raisonement) / (
                np.linalg.norm(verbe['analyse_semantique']) * np.linalg.norm(vect_raisonement))

        print(f"Verbe: {verbe['verbe']}, Lemme: {verbe['lemme']}")
        print(f"Similarité avec 'sentiments': {sentiments_similarity}")
        print(f"Similarité avec 'raisonement': {raisonement_similarity}")

        feeling += min(sentiments_similarity, 0)
        thinking += min(raisonement_similarity, 0)

        if sentiments_similarity > raisonement_similarity:
            print("F")
        else:
            print("T")

    return "feeling" if feeling > thinking else "thinking"


phrases = [("armagge", "ISTJ", "On avancera ce soir au pire."),
           ("labrique", "INFP", "ça te dérange si je t'attire dans un piège?"),
           ("labrique", "INFP", "tu sais on a quoi à manger?"),
           ("labrique", "INFP", "pourtant ici ce n'est que amour"),
           ("labrique", "INFP", "Jordan je te déteste"),
           ("labrique", "INFP", "tu es la pire personne qui existe"),
           ("labrique", "INFP", "je suis pas déséquilibré"),
           ("armagge", "ISTJ", "après c'est utilisé surtout avec des formulaires"),
           ("armagge", "ISTJ", "après justement quand je parle je suis très rarament subjectif"),
           ("armagge", "ISTJ", "Ça change pas le point consistant que j'ai la flemme")]

for personne, mbti, phrase in phrases:
    print(f"'{phrase}'({personne}, {mbti}) : {determine(phrase)}")