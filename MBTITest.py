import csv
from collections import namedtuple
import spacy

LineSet = namedtuple('LineSet', ['personality', 'lines'])


class MBTITest:
    def __init__(self):
        with open("MBTI.csv", 'r', encoding='utf-8') as csv_file:
            file = csv.reader(csv_file, delimiter='|')
            data = [LineSet(l[0], l[1]) for l in file]

            self._EI = [ls for ls in data if ls.personality == "I" or ls.personality == "E"]
            self._NS = [ls for ls in data if ls.personality == "S" or ls.personality == "N"]
            self._TF = [ls for ls in data if ls.personality == "T" or ls.personality == "F"]
            self._JP = [ls for ls in data if ls.personality == "J" or ls.personality == "P"]

        with open("thewall.csv", 'r', encoding='utf-8') as csv_file:
            file = csv.reader(csv_file, delimiter=',')
            next(file)

            data = [(l[3], l[-4], l[-3], l[-2], l[-1]) for l in file]

            self._EI += [LineSet(ls[-4], ls[0]) for ls in data if ls[-4] == "E" or ls[-4] == "I"]
            self._NS += [LineSet(ls[-3], ls[0]) for ls in data if ls[-3] == "S" or ls[-3] == "N"]
            self._TF += [LineSet(ls[-2], ls[0]) for ls in data if ls[-2] == "T" or ls[-2] == "F"]
            self._JP += [LineSet(ls[-1], ls[0]) for ls in data if ls[-1] == "J" or ls[-1] == "P"]

            counts = {}

            for tpl in self._EI + self._NS + self._TF + self._JP:
                counts[tpl.personality] = counts.get(tpl.personality, 0) + 1

            print(counts)

        self._nlp = spacy.load('fr_core_news_lg')

        self.lenght_EI = [LineSet(l.personality, self._nlp(l.lines)) for l in self._EI]
        self.lenght_NS = [LineSet(l.personality, self._nlp(l.lines)) for l in self._NS]
        self.lenght_TF = [LineSet(l.personality, self._nlp(l.lines)) for l in self._TF]
        self.lenght_JP = [LineSet(l.personality, self._nlp(l.lines)) for l in self._JP]

    def test2Lines(self, sentence1: str, sentence2):
        try:
            return self._nlp(sentence1).similarity(sentence2)
        except:
            return 0.0

    def EITest(self, sentence: str):
        message = self._nlp(sentence)

        test_value = {"E": 0.0, "I": 0.0}

        for line in self.lenght_EI:
            test_value[line.personality] += message.similarity(line.lines)

        return test_value

    def NSTest(self, sentence: str):
        message = self._nlp(sentence)

        test_value = {"N": 0.0, "S": 0.0}

        for line in self.lenght_NS:
            test_value[line.personality] += message.similarity(line.lines)

        return test_value

    def TFTest(self, sentence: str):
        message = self._nlp(sentence)

        test_value = {"T": 0.0, "F": 0.0}

        for line in self.lenght_TF:
            test_value[line.personality] += message.similarity(line.lines)

        return test_value

    def JPTest(self, sentence: str):
        message = self._nlp(sentence)

        test_value = {"J": 0.0, "P": 0.0}

        for line in self.lenght_JP:
            test_value[line.personality] += message.similarity(line.lines)

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
