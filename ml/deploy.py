import joblib
import pandas as pd

loaded_model = joblib.load('ml/model.joblib')
def is_anom(value):
    if value == 0:
        return "Normal"
    else:
        return "Anomolous"

CSV_FILE_PATH = 'db/csic_database.csv'
data = pd.read_csv(CSV_FILE_PATH)

while True:
    user_input = input(f"Input test line number (0 to {len(data)}, where seqential data change from normal to anomalous at index 36001): ")
    try:
        line = int(user_input)
        if line < 0 or line >= len(data):
            print(f"Invalid number (not within range): {line}")
            continue
    except ValueError:
        print(f"Invalid number (value error): {user_input}")
        continue

    test_data = data.iloc[line]
    test_data = pd.DataFrame([test_data])  

    print(test_data)

    test_data = test_data.drop(columns=['Unnamed: 0', 'content-type', 'lenght', 'content'])
    X = test_data.drop('classification', axis=1)

    prediction = loaded_model.predict(X)  
    print(f"Predicted classification for line {line}: {is_anom(prediction[0])}")

    actual_classification = test_data['classification'].values[0]  
    print(f"Actual classification for line {line}: {is_anom(actual_classification)}")

    # Continue??
    choice = input("Do you want to continue? (y/n): ")
    if choice.lower() != 'y':
        print("\n")
        break
