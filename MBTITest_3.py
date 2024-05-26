import csv
from collections import namedtuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

LineSet = namedtuple('LineSet', ['personality', 'lines'])


class MBTITest:
    def __init__(self):
        with open("MBTI.csv", 'r', encoding='utf-8') as csv_file:
            file = csv.reader(csv_file, delimiter='|')
            data = [LineSet(l[0], l[1]) for l in file]

        EI = [ls for ls in data if ls.personality == "I" or ls.personality == "E"]
        NS = [ls for ls in data if ls.personality == "S" or ls.personality == "N"]
        TF = [ls for ls in data if ls.personality == "T" or ls.personality == "F"]
        JP = [ls for ls in data if ls.personality == "J" or ls.personality == "P"]

        vectorizerEI = TfidfVectorizer()
        X = vectorizerEI.fit_transform([t.lines for t in EI])
        y = [t.personality for t in EI]

        modelEI = SVC()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        modelEI.fit(X_train, y_train)

        self._modelEI = modelEI
        self._vectorizerEI = vectorizerEI

        vectorizerNS = TfidfVectorizer()
        X = vectorizerNS.fit_transform([t.lines for t in NS])
        y = [t.personality for t in NS]

        modelNS = SVC()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        modelNS.fit(X_train, y_train)

        self._modelNS = modelNS
        self._vectorizerNS = vectorizerNS

        vectorizerTF = TfidfVectorizer()
        X = vectorizerTF.fit_transform([t.lines for t in TF])
        y = [t.personality for t in TF]

        modelTF = SVC()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        modelTF.fit(X_train, y_train)

        self._modelTF = modelTF
        self._vectorizerTF = vectorizerTF

        vectorizerJP = TfidfVectorizer()
        X = vectorizerJP.fit_transform([t.lines for t in JP])
        y = [t.personality for t in JP]

        modelJP = SVC()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        modelJP.fit(X_train, y_train)

        self._modelJP = modelJP
        self._vectorizerJP = vectorizerJP

    def predictEI(self, sentence: list[str]):
        new_vector = self._vectorizerEI.transform(sentence)
        predicted_type = self._modelEI.predict(new_vector)
        return predicted_type

    def predictNS(self, sentence: list[str]):
        new_vector = self._vectorizerNS.transform(sentence)
        predicted_type = self._modelNS.predict(new_vector)
        return predicted_type

    def predictTF(self, sentence: list[str]):
        new_vector = self._vectorizerTF.transform(sentence)
        predicted_type = self._modelTF.predict(new_vector)
        return predicted_type

    def predictJP(self, sentence: list[str]):
        new_vector = self._vectorizerJP.transform(sentence)
        predicted_type = self._modelJP.predict(new_vector)
        return predicted_type
