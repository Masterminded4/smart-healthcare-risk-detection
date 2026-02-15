import unittest
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_validator import validate_health_data

class TestDataValidator(unittest.TestCase):
    """Test data validation."""
    
    def test_valid_health_data(self):
        """Test validation of valid health data."""
        data = {
            'age': 45,
            'heart_rate': 78,
            'blood_pressure_systolic': 125,
            'blood_pressure_diastolic': 82,
            'bmi': 26.5,
            'exercise_frequency': 2,
            'smoking': False,
            'symptoms': ['chest pain'],
            'family_history': ['hypertension']
        }
        
        is_valid, errors = validate_health_data(data)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_missing_required_fields(self):
        """Test validation with missing fields."""
        data = {
            'age': 45,
            'heart_rate': 78
        }
        
        is_valid, errors = validate_health_data(data)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_invalid_age(self):
        """Test validation of invalid age."""
        data = {
            'age': 200,
            'heart_rate': 78,
            'blood_pressure_systolic': 125,
            'blood_pressure_diastolic': 82,
            'bmi': 26.5
        }
        
        is_valid, errors = validate_health_data(data)
        self.assertFalse(is_valid)
    
    def test_invalid_heart_rate(self):
        """Test validation of invalid heart rate."""
        data = {
            'age': 45,
            'heart_rate': 300,
            'blood_pressure_systolic': 125,
            'blood_pressure_diastolic': 82,
            'bmi': 26.5
        }
        
        is_valid, errors = validate_health_data(data)
        self.assertFalse(is_valid)
    
    def test_invalid_bmi(self):
        """Test validation of invalid BMI."""
        data = {
            'age': 45,
            'heart_rate': 78,
            'blood_pressure_systolic': 125,
            'blood_pressure_diastolic': 82,
            'bmi': 100
        }
        
        is_valid, errors = validate_health_data(data)
        self.assertFalse(is_valid)

if __name__ == '__main__':
    unittest.main()