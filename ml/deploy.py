import joblib
import pandas as pd

class AnomalyDetector:
    def __init__(self, model_path='ml/model.joblib', csv_file_path='db/csic_database.csv'):
        self.model = joblib.load(model_path)
        self.data = pd.read_csv(csv_file_path)
        
    @staticmethod
    def is_anom(value):
        return "Normal" if value == 0 else "Anomalous"
    
    def run_test(self):
        while True:
            user_input = input(f"Input test line number (0 to {len(self.data)}, where seqential data change from normal to anomalous at index 36001): ")
            try:
                line = int(user_input)
                if line < 0 or line >= len(self.data):
                    print(f"Invalid number (not within range): {line}")
                    continue
            except ValueError:
                print(f"Invalid number (value error): {user_input}")
                continue

            test_data = self.data.iloc[line]
            test_data = pd.DataFrame([test_data])  

            print(test_data)

            test_data = test_data.drop(columns=['Unnamed: 0', 'content-type', 'lenght', 'content'])
            X = test_data.drop('classification', axis=1)

            prediction = self.model.predict(X)  
            print(f"Predicted classification for line {line}: {self.is_anom(prediction[0])}")

            actual_classification = test_data['classification'].values[0]  
            print(f"Actual classification for line {line}: {self.is_anom(actual_classification)}")

            user_input = input("Enter 'y' to leave or any other key to continue: ").strip().lower()
            if user_input == 'y':
                print("Exiting the loop...")
                break

    def predict_anomaly(self, data):
        X = pd.DataFrame([data])
        prediction = self.model.predict(X)
        return self.is_anom(prediction[0])