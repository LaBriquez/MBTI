from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def determine_sentiment(sentence):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(sentence)
    return sentiment_scores


phrases = [
    "no it's impossible",
    "Good soldiers follow orders",
    "do or don't do it, there are no try",
    "unlimited power",
    "you are with me, or you are against me",
    "You were the chosen one it was you",
    "I hate you"
]

for phrase in phrases:
    sentiment_score = determine_sentiment(phrase)
    print(f"La phrase '{phrase}' a un score de sentiment de {sentiment_score}")