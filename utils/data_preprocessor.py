import pandas as pd

class DataPreprocessor:
    def preprocess(self, data_path):
        data = pd.read_csv(data_path)
        # Example preprocessing steps
        data.fillna(0, inplace=True)
        data.drop_duplicates(inplace=True)
        return data

if __name__ == "__main__":
    preprocessor = DataPreprocessor()
    processed_data = preprocessor.preprocess('./data/training_data.csv')
    print(processed_data.head())
