import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

# Charger les données CSV
df = pd.read_csv('votre_fichier.csv', header=None, names=['Type', 'Phrase'])

# Créer une matrice de features en utilisant CountVectorizer
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['Phrase'])

# Diviser les données en ensemble d'entraînement et ensemble de test
X_train, X_test, y_train, y_test = train_test_split(X, df['Type'], test_size=0.2, random_state=42)

# Appliquer SMOTE pour équilibrer les classes
smote = SMOTE()
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# Rétablir les données équilibrées dans un DataFrame
balanced_df = pd.DataFrame(X_train_resampled.toarray(), columns=vectorizer.get_feature_names_out())
balanced_df['Type'] = y_train_resampled

# Maintenant vous pouvez utiliser balanced_df pour l'entraînement de votre modèle