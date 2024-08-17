import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

class BehaviorAnalysis:
    def __init__(self):
        self.model = RandomForestClassifier()

    def train_model(self, data_path):
        data = pd.read_csv(data_path)
        X = data.drop('anomaly', axis=1)
        y = data['anomaly']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        print(classification_report(y_test, predictions))
        joblib.dump(self.model, './data/models/behavior_model.pkl')

    def predict(self, features):
        model = joblib.load('./data/models/behavior_model.pkl')
        return model.predict([features])[0]

if __name__ == "__main__":
    analysis = BehaviorAnalysis()
    analysis.train_model('./data/training_data.csv')
