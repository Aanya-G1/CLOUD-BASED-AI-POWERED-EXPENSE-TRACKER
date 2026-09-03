import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib



def train_and_save_model():

    data = pd.read_csv("expenses_dataset.csv")


    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(data['description'])
    y = data['category']


    model = MultinomialNB()
    model.fit(X, y)


    joblib.dump(model, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    print("Model and vectorizer saved successfully.")

if __name__ == "__main__":
    train_and_save_model()
