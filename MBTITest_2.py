from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split


class MBTITest:
    def __init__(self):
        data = [
            {"text": "Je suis extraverti, aime être au centre de l'attention.", "type": "ENFJ"},
            {"text": "Je préfère travailler seul et éviter les grands groupes.", "type": "ISTP"},
            {"text": "Je préfère suivre des instructions claires et précises dans mon travail.", "type": "ISTJ"},
            {"text": "J'aime aider les autres et je suis très attentif à leurs besoins émotionnels.", "type": "ISFJ"},
            {"text": "Je suis empathique et j'ai un fort sens de la compassion envers les autres.", "type": "INFJ"},
            {"text": "Je suis stratégique et j'ai une vision à long terme dans mes plans.", "type": "INTJ"},
            {"text": "Je suis artistique et j'exprime mes émotions à travers différentes formes d'art.",
             "type": "ISFP"},
            {"text": "Je suis idéaliste et je crois en la bonté intrinsèque des gens.", "type": "INFP"},
            {"text": "Je suis très courageux et j'aime prendre des risques calculés.", "type": "ESTP"},
            {"text": "Je suis très spontané et j'apprécie les plaisirs simples de la vie.", "type": "ESFP"},
            {"text": "Je suis très enthousiaste et j'aime inspirer les autres avec mes idées créatives.",
             "type": "ENFP"},
            {"text": "Je suis très inventif et j'aime trouver des solutions innovantes aux problèmes.", "type": "ENTP"},
            {"text": "Je suis très organisé et j'aime planifier chaque détail de mes activités.", "type": "ESTJ"},
            {
                "text": "Je suis très attentionné envers les autres et je fais de mon mieux pour répondre à leurs besoins émotionnels.",
                "type": "ESFJ"},
            {"text": "Je suis très ambitieux et j'ai une vision claire de mes objectifs à long terme.", "type": "ENTJ"},
            {"text": "Je suis curieux et j'aime explorer de nouvelles idées et concepts.", "type": "INTP"}
        ]

        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform([d["text"] for d in data])
        y = [d["type"] for d in data]

        model = SVC()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model.fit(X_train, y_train)

        self._model = model
        self._vectorizer = vectorizer

    def test_sentence(self, sentence: list[str]):
        new_vector = self._vectorizer.transform(sentence)
        predicted_type = self._model.predict(new_vector)
        return predicted_type
