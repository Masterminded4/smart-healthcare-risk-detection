from models.risk_predictor import RiskPredictor
from utils.logger import setup_logger
from datetime import datetime
import json

logger = setup_logger(__name__)

class PredictionService:
    def __init__(self):
        self.predictor = RiskPredictor()
        self.assessment_history = {}
    
    def assess_risk(self, health_data):
        """Perform risk assessment."""
        try:
            result = self.predictor.predict_risk(health_data)
            result['timestamp'] = datetime.now().isoformat()
            result['health_inputs'] = health_data
            
            # Store in history
            user_id = health_data.get('user_id', 'anonymous')
            if user_id not in self.assessment_history:
                self.assessment_history[user_id] = []
            
            self.assessment_history[user_id].append(result)
            
            return result
        except Exception as e:
            logger.error(f"Risk assessment error: {str(e)}")
            raise
    
    def generate_precautions(self, diseases, age, lifestyle, conditions):
        """Generate personalized precautions."""
        precautions = {
            "immediate_actions": [],
            "short_term_changes": [],
            "long_term_lifestyle": [],
            "monitoring": [],
            "specialist_referrals": []
        }
        
        # Disease-specific precautions
        disease_precautions = {
            "Hypertension": {
                "immediate": ["Check blood pressure immediately", "Reduce sodium intake"],
                "referral": "Cardiologist"
            },
            "Diabetes": {
                "immediate": ["Get blood glucose test", "Review diet"],
                "referral": "Endocrinologist"
            },
            "Stroke Risk": {
                "immediate": ["Seek emergency care", "Monitor symptoms"],
                "referral": "Neurologist"
            }
        }
        
        for disease in diseases:
            if disease in disease_precautions:
                precautions["immediate_actions"].extend(
                    disease_precautions[disease].get("immediate", [])
                )
                precautions["specialist_referrals"].append(
                    disease_precautions[disease].get("referral")
                )
        
        # Lifestyle recommendations
        if lifestyle == "sedentary":
            precautions["short_term_changes"].extend([
                "Start with 15 minutes of walking daily",
                "Use stairs instead of elevators",
                "Do stretching exercises"
            ])
        
        if "overweight" in conditions:
            precautions["long_term_lifestyle"].extend([
                "Aim for 150 minutes moderate exercise per week",
                "Reduce processed foods",
                "Drink at least 2 liters of water daily"
            ])
        
        precautions["monitoring"] = [
            "Weekly blood pressure checks",
            "Monthly weight monitoring",
            "Quarterly health check-ups"
        ]
        
        return precautions
    
    def get_user_history(self, user_id):
        """Get user's assessment history."""
        return self.assessment_history.get(user_id, [])
    
    def get_lifestyle_tips(self):
        """Get general lifestyle improvement tips."""
        return {
            "nutrition": [
                "Eat 5 servings of fruits and vegetables daily",
                "Limit sugar to <25g per day",
                "Choose whole grains over refined carbs"
            ],
            "exercise": [
                "Aim for 150 minutes of moderate aerobic activity weekly",
                "Include strength training 2 days per week",
                "Practice flexibility exercises"
            ],
            "sleep": [
                "Maintain consistent sleep schedule (7-9 hours)",
                "Avoid screens 1 hour before bed",
                "Keep bedroom cool and dark"
            ],
            "stress": [
                "Practice meditation or yoga",
                "Limit caffeine intake",
                "Spend time in nature"
            ],
            "monitoring": [
                "Track vital signs regularly",
                "Keep health records updated",
                "Schedule annual health check-ups"
            ]
        }