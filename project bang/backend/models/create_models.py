import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib

def generate_training_data():
    # Generate synthetic data
    num_samples = 1000
    X = np.random.rand(num_samples, 10)  # Features
    y = np.random.randint(0, 2, size=num_samples)  # Binary target

    # Create DataFrame
    data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])
    data['target'] = y
    return data

def train_model(data):
    # Split data into features and target
    X = data.drop('target', axis=1)
    y = data['target']

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Save model and scaler
    joblib.dump(model, 'disease_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')

if __name__ == '__main__':
    training_data = generate_training_data()
    train_model(training_data)
