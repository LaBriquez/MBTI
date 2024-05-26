import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, SpatialDropout1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def test_with(data, sentence_test, test_size):
  X = data['sentence']
  y = data['MBTI']

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

  tfidf_vectorizer = TfidfVectorizer()
  X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
  X_test_tfidf = tfidf_vectorizer.transform(sentence_test)

  rf_classifier = RandomForestClassifier()
  rf_classifier.fit(X_train_tfidf, y_train)

  svm_classifier = SVC(kernel='linear')
  svm_classifier.fit(X_train_tfidf, y_train)

  nb_classifier = MultinomialNB()
  nb_classifier.fit(X_train_tfidf, y_train)

  lr_classifier = LogisticRegression()
  lr_classifier.fit(X_train_tfidf, y_train)

  gbm_classifier = GradientBoostingClassifier()
  gbm_classifier.fit(X_train_tfidf, y_train)

  rf_pred = rf_classifier.predict(X_test_tfidf)
  svm_pred = svm_classifier.predict(X_test_tfidf)
  nb_pred = nb_classifier.predict(X_test_tfidf)
  lr_pred = lr_classifier.predict(X_test_tfidf)
  gbm_pred = gbm_classifier.predict(X_test_tfidf)

  print("Random Forest:", rf_pred)
  print("Support Vector Machines:", svm_pred)
  print("Naive Bayes:", nb_pred)
  print("Logistic Regression:", lr_pred)
  print("Gradient Boosting Machines:", gbm_pred)

  print("Random Forest Accuracy:", accuracy_score(y_test, rf_pred))
  print("Support Vector Machines Accuracy:", accuracy_score(y_test, svm_pred))
  print("Naive Bayes Accuracy:", accuracy_score(y_test, nb_pred))
  print("Logistic Regression Accuracy:", accuracy_score(y_test, lr_pred))
  print("Gradient Boosting Machines Accuracy:", accuracy_score(y_test, gbm_pred))

def test_data(datas, tests):
  for d in datas:
    for i in range(1, 1000):
      print(f"test with {i / 1000}, {data[0]}")
      test_with(data[1], tests, i / 1000)