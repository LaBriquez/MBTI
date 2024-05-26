import csv
from collections import namedtuple
import spacy

LineSet = namedtuple('LineSet', ['personality', 'lines'])


class MBTITest:
    def __init__(self):
        with open("MBTI.csv", 'r', encoding='utf-8') as csv_file:
            file = csv.reader(csv_file, delimiter='|')
            data = [LineSet(l[0], l[1]) for l in file]

        self._nlp = spacy.load('fr_core_news_lg')

        self._EI = [ls for ls in data if ls.personality == "I" or ls.personality == "E"]
        self._NS = [ls for ls in data if ls.personality == "S" or ls.personality == "N"]
        self._TF = [ls for ls in data if ls.personality == "T" or ls.personality == "F"]
        self._JP = [ls for ls in data if ls.personality == "J" or ls.personality == "P"]

    def test2Lines(self, sentence1: str, sentence2: str):
        try:
            return self._nlp(sentence1).similarity(self._nlp(sentence2))
        except:
            return 0.0

    def EITest(self, sentence: str):
        message = self._nlp(sentence)

        test_value = {"E": 0.0, "I": 0.0}

        for line in self._EI:
            test_value[line.personality] += message.similarity(self._nlp(line.lines))

        return test_value

    def NSTest(self, sentence: str):
        message = self._nlp(sentence)

        test_value = {"N": 0.0, "S": 0.0}

        for line in self._NS:
            test_value[line.personality] += message.similarity(self._nlp(line.lines))

        return test_value

    def TFTest(self, sentence: str):
        message = self._nlp(sentence)

        test_value = {"T": 0.0, "F": 0.0}

        for line in self._TF:
            test_value[line.personality] += message.similarity(self._nlp(line.lines))

        return test_value

    def JPTest(self, sentence: str):
        message = self._nlp(sentence)

        test_value = {"J": 0.0, "P": 0.0}

        for line in self._JP:
            test_value[line.personality] += message.similarity(self._nlp(line.lines))

        return test_value

    def MBTITest(self, message: str):
        testEI = self.EITest(message)
        testNS = self.NSTest(message)
        testTF = self.TFTest(message)
        testJP = self.JPTest(message)

        return {
            "E": testEI["E"], "I": testEI["I"],
            "N": testNS["N"], "S": testNS["S"],
            "T": testTF["T"], "F": testTF["F"],
            "J": testJP["J"], "P": testJP["P"],
            }

    def MBTIadder(self, values: dict[str, float], message: str):
        test = self.MBTITest(message)
        for k in values.keys():
            values[k] += test[k]
