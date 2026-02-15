import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
from pathlib import Path

class RiskPredictor:
    def __init__(self, model_path=None, scaler_path=None):
        self.model_path = model_path or Path(__file__).parent / 'disease_model.pkl'
        self.scaler_path = scaler_path or Path(__file__).parent / 'scaler.pkl'
        
        try:
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
        except FileNotFoundError:
            self.model = None
            self.scaler = None
    
    def predict_risk(self, health_data):
        """
        Predict disease risk based on health inputs.
        
        Args:
            health_data: dict with keys:
                - heart_rate: int (bpm)
                - blood_pressure_systolic: int (mmHg)
                - blood_pressure_diastolic: int (mmHg)
                - age: int
                - bmi: float
                - symptoms: list of strings
                - smoking: bool
                - exercise_frequency: int (days/week)
                - family_history: list of diseases
        
        Returns:
            dict with risk assessments
        """
        if self.model is None:
            raise RuntimeError("Model not trained. Please train the model first.")
        
        # Feature engineering
        features = self._extract_features(health_data)
        
        # Scale features
        features_scaled = self.scaler.transform([features])
        
        # Get predictions and probabilities
        risk_prediction = self.model.predict(features_scaled)[0]
        risk_probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Map to disease classes
        diseases = self.model.classes_
        risk_scores = {
            disease: float(prob) 
            for disease, prob in zip(diseases, risk_probabilities)
        }
        
        # Identify high-risk conditions (>40% probability)
        high_risk_diseases = [
            disease for disease, score in risk_scores.items() 
            if score > 0.4
        ]
        
        return {
            "overall_risk_level": self._calculate_risk_level(risk_scores),
            "risk_scores": risk_scores,
            "high_risk_diseases": high_risk_diseases,
            "primary_concern": max(risk_scores, key=risk_scores.get),
            "recommendation": self._get_recommendation(high_risk_diseases, health_data)
        }
    
    def _extract_features(self, health_data):
        """Extract and normalize features from health data."""
        features = [
            health_data.get('age', 30),
            health_data.get('heart_rate', 70),
            health_data.get('blood_pressure_systolic', 120),
            health_data.get('blood_pressure_diastolic', 80),
            health_data.get('bmi', 24),
            health_data.get('exercise_frequency', 3),
            int(health_data.get('smoking', False)),
            len(health_data.get('symptoms', [])),
            len(health_data.get('family_history', [])),
        ]
        return features
    
    def _calculate_risk_level(self, risk_scores):
        """Calculate overall risk level."""
        max_risk = max(risk_scores.values())
        if max_risk > 0.7:
            return "CRITICAL"
        elif max_risk > 0.5:
            return "HIGH"
        elif max_risk > 0.3:
            return "MODERATE"
        else:
            return "LOW"
    
    def _get_recommendation(self, diseases, health_data):
        """Generate recommendations based on risks."""
        if not diseases:
            return "Maintain healthy lifestyle and regular check-ups."
        
        recommendations = []
        
        if "Cardiovascular Disease" in diseases:
            recommendations.append("Consult a cardiologist immediately")
            recommendations.append("Monitor blood pressure daily")
            recommendations.append("Reduce salt and saturated fat intake")
        
        if "Diabetes" in diseases:
            recommendations.append("Get blood glucose testing")
            recommendations.append("Monitor dietary intake")
            recommendations.append("Increase physical activity")
        
        if "Stroke Risk" in diseases:
            recommendations.append("Emergency medical evaluation recommended")
            recommendations.append("Take aspirin if recommended by doctor")
        
        if health_data.get('smoking'):
            recommendations.append("Quit smoking immediately")
        
        return recommendations
    
    def train_model(self, X_train, y_train, X_test, y_test):
        """Train the risk prediction model."""
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Save models
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        
        score = self.model.score(X_test_scaled, y_test)
        return {"accuracy": score, "model_saved": True}