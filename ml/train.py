import joblib
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
import matplotlib
matplotlib.use('Agg')

CSV_FILE_PATH = 'db/csic_database.csv'

data = pd.read_csv(CSV_FILE_PATH)
print(data.head())
data = data.drop(columns=['Unnamed: 0', 'content-type', 'lenght', 'content']) # Drop columns that we don't need or have no data

X = data.drop('classification', axis=1) 
y = data['classification'] 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

categorical_columns = ['Method', 'User-Agent', 'Pragma', 'Cache-Control', 'Accept', 'Accept-encoding', 'Accept-charset', 'language', 'host', 'cookie', 'connection', 'URL']
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_columns)
    ])
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train
model.fit(X_train, y_train)
joblib.dump(model, 'ml/model.joblib')
# # Run Model
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

