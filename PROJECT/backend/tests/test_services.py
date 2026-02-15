"""
Comprehensive test suite for backend services.
Tests prediction_service, geolocation_service, and notification_service.
"""

import unittest
import json
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.prediction_service import PredictionService
from services.geolocation_service import GeoLocationService
from services.notification_service import NotificationService


class TestPredictionService(unittest.TestCase):
    """Test suite for PredictionService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = PredictionService()
    
    def test_service_initialization(self):
        """Test service initializes correctly."""
        self.assertIsNotNone(self.service.predictor)
        self.assertIsNotNone(self.service.assessment_history)
        self.assertEqual(len(self.service.assessment_history), 0)
    
    def test_assess_risk_valid_data(self):
        """Test risk assessment with valid data."""
        health_data = {
            'age': 45,
            'heart_rate': 78,
            'blood_pressure_systolic': 125,
            'blood_pressure_diastolic': 82,
            'bmi': 26.5,
            'exercise_frequency': 2,
            'smoking': False,
            'symptoms': ['chest pain'],
            'family_history': ['hypertension'],
            'user_id': 'test_user_1'
        }
        
        result = self.service.assess_risk(health_data)
        
        # Verify result structure
        self.assertIn('overall_risk_level', result)
        self.assertIn('risk_scores', result)
        self.assertIn('high_risk_diseases', result)
        self.assertIn('primary_concern', result)
        self.assertIn('recommendation', result)
        self.assertIn('timestamp', result)
        self.assertIn('health_inputs', result)
    
    def test_assess_risk_stores_history(self):
        """Test that assessment is stored in history."""
        health_data = {
            'age': 45,
            'heart_rate': 78,
            'blood_pressure_systolic': 125,
            'blood_pressure_diastolic': 82,
            'bmi': 26.5,
            'exercise_frequency': 2,
            'smoking': False,
            'symptoms': [],
            'family_history': [],
            'user_id': 'test_user_2'
        }
        
        self.service.assess_risk(health_data)
        
        # Check history was stored
        history = self.service.get_user_history('test_user_2')
        self.assertEqual(len(history), 1)
    
    def test_assess_risk_multiple_assessments(self):
        """Test multiple assessments for same user."""
        user_id = 'test_user_3'
        
        # First assessment
        data1 = {
            'age': 40,
            'heart_rate': 70,
            'blood_pressure_systolic': 120,
            'blood_pressure_diastolic': 80,
            'bmi': 24,
            'exercise_frequency': 3,
            'smoking': False,
            'symptoms': [],
            'family_history': [],
            'user_id': user_id
        }
        self.service.assess_risk(data1)
        
        # Second assessment
        data2 = {
            'age': 40,
            'heart_rate': 85,
            'blood_pressure_systolic': 135,
            'blood_pressure_diastolic': 90,
            'bmi': 26,
            'exercise_frequency': 2,
            'smoking': True,
            'symptoms': ['fatigue'],
            'family_history': ['diabetes'],
            'user_id': user_id
        }
        self.service.assess_risk(data2)
        
        # Verify both stored
        history = self.service.get_user_history(user_id)
        self.assertEqual(len(history), 2)
    
    def test_get_user_history_nonexistent(self):
        """Test getting history for user with no assessments."""
        history = self.service.get_user_history('nonexistent_user')
        self.assertEqual(history, [])
    
    def test_generate_precautions_cardiovascular(self):
        """Test precautions for cardiovascular disease."""
        precautions = self.service.generate_precautions(
            diseases=['Cardiovascular Disease'],
            age=50,
            lifestyle='sedentary',
            conditions=['overweight']
        )
        
        self.assertIn('immediate_actions', precautions)
        self.assertIn('short_term_changes', precautions)
        self.assertIn('long_term_lifestyle', precautions)
        self.assertIn('monitoring', precautions)
        self.assertIn('specialist_referrals', precautions)
        
        # Check cardiovascular-specific actions
        self.assertTrue(any(
            'cardiologist' in str(action).lower()
            for action in precautions['immediate_actions']
        ))
    
    def test_generate_precautions_diabetes(self):
        """Test precautions for diabetes."""
        precautions = self.service.generate_precautions(
            diseases=['Diabetes'],
            age=50,
            lifestyle='sedentary',
            conditions=[]
        )
        
        self.assertIn('specialist_referrals', precautions)
        self.assertIn('Endocrinologist', precautions['specialist_referrals'])
    
    def test_generate_precautions_multiple_diseases(self):
        """Test precautions for multiple diseases."""
        precautions = self.service.generate_precautions(
            diseases=['Hypertension', 'Diabetes', 'Stroke Risk'],
            age=60,
            lifestyle='sedentary',
            conditions=['overweight']
        )
        
        # Should have referrals for all three
        self.assertGreaterEqual(len(precautions['specialist_referrals']), 3)
    
    def test_generate_precautions_sedentary_lifestyle(self):
        """Test exercise recommendations for sedentary lifestyle."""
        precautions = self.service.generate_precautions(
            diseases=[],
            age=45,
            lifestyle='sedentary',
            conditions=[]
        )
        
        # Should recommend starting exercise
        self.assertTrue(any(
            'walk' in str(action).lower()
            for action in precautions['short_term_changes']
        ))
    
    def test_generate_precautions_overweight(self):
        """Test weight management recommendations."""
        precautions = self.service.generate_precautions(
            diseases=[],
            age=45,
            lifestyle='active',
            conditions=['overweight']
        )
        
        # Should recommend exercise and diet
        lifestyle_recs = precautions['long_term_lifestyle']
        self.assertTrue(any(
            'exercise' in str(rec).lower() or '150' in str(rec)
            for rec in lifestyle_recs
        ))
    
    def test_get_lifestyle_tips_structure(self):
        """Test lifestyle tips have correct structure."""
        tips = self.service.get_lifestyle_tips()
        
        expected_categories = [
            'nutrition', 'exercise', 'sleep', 'stress', 'monitoring'
        ]
        
        for category in expected_categories:
            self.assertIn(category, tips)
            self.assertIsInstance(tips[category], list)
            self.assertGreater(len(tips[category]), 0)
    
    def test_get_lifestyle_tips_content(self):
        """Test lifestyle tips contain relevant advice."""
        tips = self.service.get_lifestyle_tips()
        
        # Nutrition tips
        self.assertTrue(any(
            'fruit' in str(tip).lower() or 'vegetable' in str(tip).lower()
            for tip in tips['nutrition']
        ))
        
        # Exercise tips
        self.assertTrue(any(
            '150' in str(tip)
            for tip in tips['exercise']
        ))
        
        # Sleep tips
        self.assertTrue(any(
            'hour' in str(tip).lower()
            for tip in tips['sleep']
        ))


class TestGeolocationService(unittest.TestCase):
    """Test suite for GeoLocationService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = GeoLocationService()
    
    def test_service_initialization(self):
        """Test service initializes with hospitals."""
        self.assertIsNotNone(self.service.hospitals)
        self.assertGreater(len(self.service.hospitals), 0)
    
    def test_hospital_data_structure(self):
        """Test hospital data has required fields."""
        required_fields = [
            'id', 'name', 'latitude', 'longitude', 'address',
            'phone', 'specialties', 'has_icu', 'rating', 'availability'
        ]
        
        for hospital in self.service.hospitals:
            for field in required_fields:
                self.assertIn(field, hospital, f"Missing field: {field}")
    
    def test_find_hospitals_nearby(self):
        """Test finding hospitals near a location."""
        hospitals = self.service.find_hospitals(
            latitude=40.7128,
            longitude=-74.0060,
            radius_km=15
        )
        
        self.assertIsInstance(hospitals, list)
        self.assertGreater(len(hospitals), 0)
    
    def test_find_hospitals_with_distance(self):
        """Test that returned hospitals have distance calculated."""
        hospitals = self.service.find_hospitals(
            latitude=40.7128,
            longitude=-74.0060,
            radius_km=15
        )
        
        for hospital in hospitals:
            self.assertIn('distance', hospital)
            self.assertGreater(hospital['distance'], 0)
            self.assertLessEqual(hospital['distance'], 15)
    
    def test_find_hospitals_sorted_by_distance(self):
        """Test hospitals are sorted by distance."""
        hospitals = self.service.find_hospitals(
            latitude=40.7128,
            longitude=-74.0060,
            radius_km=15
        )
        
        if len(hospitals) > 1:
            for i in range(len(hospitals) - 1):
                self.assertLessEqual(
                    hospitals[i]['distance'],
                    hospitals[i + 1]['distance']
                )
    
    def test_find_hospitals_filter_by_specialty(self):
        """Test filtering hospitals by specialty."""
        hospitals = self.service.find_hospitals(
            latitude=40.7128,
            longitude=-74.0060,
            radius_km=15,
            specialty='cardiology'
        )
        
        for hospital in hospitals:
            self.assertTrue(any(
                'cardiology' in str(spec).lower()
                for spec in hospital['specialties']
            ))
    
    def test_find_hospitals_urgency_high(self):
        """Test high urgency prioritizes ICU hospitals."""
        hospitals = self.service.find_hospitals(
            latitude=40.7128,
            longitude=-74.0060,
            radius_km=15,
            urgency='high'
        )
        
        # First hospital should preferably have ICU
        if hospitals:
            self.assertTrue(hospitals[0]['has_icu'])
    
    def test_find_hospitals_radius_constraint(self):
        """Test radius constraint is respected."""
        hospitals = self.service.find_hospitals(
            latitude=40.7128,
            longitude=-74.0060,
            radius_km=5  # Small radius
        )
        
        # All returned hospitals should be within radius
        for hospital in hospitals:
            self.assertLessEqual(hospital['distance'], 5)
    
    def test_find_hospitals_no_results(self):
        """Test when no hospitals found in radius."""
        hospitals = self.service.find_hospitals(
            latitude=40.7128,
            longitude=-74.0060,
            radius_km=0.1  # Very small radius
        )
        
        # May or may not have results, but should not error
        self.assertIsInstance(hospitals, list)
    
    def test_find_emergency_hospitals(self):
        """Test finding emergency hospitals."""
        hospitals = self.service.find_emergency_hospitals(
            latitude=40.7128,
            longitude=-74.0060,
            count=3
        )
        
        self.assertIsInstance(hospitals, list)
        self.assertLessEqual(len(hospitals), 3)
        
        # All should be emergency hospitals
        for hospital in hospitals:
            self.assertTrue(any(
                'emergency' in str(spec).lower()
                for spec in hospital['specialties']
            ))
    
    def test_find_emergency_hospitals_sorted(self):
        """Test emergency hospitals are sorted by distance."""
        hospitals = self.service.find_emergency_hospitals(
            latitude=40.7128,
            longitude=-74.0060,
            count=5
        )
        
        if len(hospitals) > 1:
            for i in range(len(hospitals) - 1):
                self.assertLessEqual(
                    hospitals[i]['distance'],
                    hospitals[i + 1]['distance']
                )
    
    def test_get_hospital_details(self):
        """Test getting specific hospital details."""
        hospital = self.service.get_hospital_details(1)
        
        if hospital:
            self.assertEqual(hospital['id'], 1)
            self.assertIn('name', hospital)
    
    def test_get_hospital_details_nonexistent(self):
        """Test getting nonexistent hospital."""
        hospital = self.service.get_hospital_details(9999)
        self.assertIsNone(hospital)


class TestNotificationService(unittest.TestCase):
    """Test suite for NotificationService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = NotificationService()
    
    def test_service_initialization(self):
        """Test service initializes correctly."""
        self.assertIsNotNone(self.service.smtp_server)
        self.assertIsNotNone(self.service.smtp_port)
    
    @patch('services.notification_service.smtplib.SMTP')
    def test_send_risk_alert_high_risk(self, mock_smtp):
        """Test sending high-risk alert."""
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
        
        risk_data = {
            'overall_risk_level': 'HIGH',
            'primary_concern': 'Cardiovascular Disease',
            'risk_scores': {
                'Cardiovascular Disease': 0.72,
                'Diabetes': 0.45,
                'Stroke Risk': 0.38,
                'Healthy': 0.12
            },
            'recommendation': [
                'Consult a cardiologist',
                'Monitor blood pressure'
            ]
        }
        
        # Note: Notifications disabled by default in tests
        result = self.service.send_risk_alert(
            'patient@example.com',
            risk_data
        )
        
        # Should return result based on ENABLE_NOTIFICATIONS config
        self.assertIsInstance(result, bool)
    
    @patch('services.notification_service.smtplib.SMTP')
    def test_send_risk_alert_critical_risk(self, mock_smtp):
        """Test sending critical-risk alert."""
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
        
        risk_data = {
            'overall_risk_level': 'CRITICAL',
            'primary_concern': 'Stroke Risk',
            'risk_scores': {
                'Stroke Risk': 0.85,
                'Cardiovascular Disease': 0.72,
                'Diabetes': 0.45,
                'Healthy': 0.05
            },
            'recommendation': [
                'Emergency medical evaluation',
                'Call ambulance'
            ]
        }
        
        result = self.service.send_risk_alert(
            'critical_patient@example.com',
            risk_data
        )
        
        self.assertIsInstance(result, bool)
    
    def test_format_risk_scores(self):
        """Test formatting risk scores for email."""
        scores = {
            'Cardiovascular Disease': 0.72,
            'Diabetes': 0.45,
            'Stroke Risk': 0.38,
            'Healthy': 0.12
        }
        
        formatted = self.service._format_risk_scores(scores)
        
        self.assertIn('Cardiovascular Disease', formatted)
        self.assertIn('72.0%', formatted)
    
    def test_format_recommendations_list(self):
        """Test formatting recommendations list."""
        recommendations = [
            'Consult a cardiologist',
            'Monitor blood pressure',
            'Reduce salt intake'
        ]
        
        formatted = self.service._format_recommendations(recommendations)
        
        for rec in recommendations:
            self.assertIn(rec, formatted)
    
    def test_format_recommendations_string(self):
        """Test formatting single recommendation string."""
        recommendation = 'Consult a doctor'
        
        formatted = self.service._format_recommendations(recommendation)
        
        self.assertIn('Consult a doctor', formatted)


class TestServiceIntegration(unittest.TestCase):
    """Integration tests for multiple services working together."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.prediction_service = PredictionService()
        self.geolocation_service = GeoLocationService()
    
    def test_complete_assessment_workflow(self):
        """Test complete assessment and hospital finding workflow."""
        # Step 1: Assess health
        health_data = {
            'age': 50,
            'heart_rate': 88,
            'blood_pressure_systolic': 140,
            'blood_pressure_diastolic': 90,
            'bmi': 28,
            'exercise_frequency': 1,
            'smoking': True,
            'symptoms': ['chest pain', 'shortness of breath'],
            'family_history': ['hypertension', 'heart disease'],
            'latitude': 40.7128,
            'longitude': -74.0060,
            'user_id': 'integration_test_1'
        }
        
        assessment = self.prediction_service.assess_risk(health_data)
        
        self.assertIn('overall_risk_level', assessment)
        self.assertNotEqual(assessment['overall_risk_level'], 'LOW')
        
        # Step 2: Find nearby hospitals
        hospitals = self.geolocation_service.find_hospitals(
            latitude=health_data['latitude'],
            longitude=health_data['longitude'],
            radius_km=15,
            urgency='high'
        )
        
        self.assertGreater(len(hospitals), 0)
        
        # Step 3: Generate precautions
        precautions = self.prediction_service.generate_precautions(
            diseases=assessment['high_risk_diseases'],
            age=health_data['age'],
            lifestyle='sedentary' if health_data['exercise_frequency'] < 3 else 'active',
            conditions=[]
        )
        
        self.assertIn('specialist_referrals', precautions)
    
    def test_low_risk_patient_workflow(self):
        """Test workflow for low-risk patient."""
        health_data = {
            'age': 25,
            'heart_rate': 65,
            'blood_pressure_systolic': 110,
            'blood_pressure_diastolic': 70,
            'bmi': 22,
            'exercise_frequency': 5,
            'smoking': False,
            'symptoms': [],
            'family_history': [],
            'latitude': 40.7128,
            'longitude': -74.0060,
            'user_id': 'integration_test_2'
        }
        
        assessment = self.prediction_service.assess_risk(health_data)
        
        # Low-risk patients should have few or no high-risk diseases
        self.assertEqual(assessment['overall_risk_level'], 'LOW')
        self.assertEqual(len(assessment['high_risk_diseases']), 0)


class TestServiceErrorHandling(unittest.TestCase):
    """Test error handling in services."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.prediction_service = PredictionService()
        self.geolocation_service = GeoLocationService()
    
    def test_prediction_service_handles_missing_fields(self):
        """Test prediction service handles missing optional fields."""
        health_data = {
            'age': 45,
            'heart_rate': 78,
            'blood_pressure_systolic': 125,
            'blood_pressure_diastolic': 82,
            'bmi': 26.5,
            'exercise_frequency': 2,
            'smoking': False
            # Missing symptoms and family_history
        }
        
        try:
            result = self.prediction_service.assess_risk(health_data)
            self.assertIn('overall_risk_level', result)
        except KeyError:
            self.fail("Service should handle missing optional fields")
    
    def test_geolocation_service_handles_invalid_coordinates(self):
        """Test geolocation service handles invalid coordinates gracefully."""
        # Invalid latitude
        hospitals = self.geolocation_service.find_hospitals(
            latitude=150,  # Invalid
            longitude=-74.0060,
            radius_km=15
        )
        
        # Should return empty or handle gracefully
        self.assertIsInstance(hospitals, list)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPredictionService))
    suite.addTests(loader.loadTestsFromTestCase(TestGeolocationService))
    suite.addTests(loader.loadTestsFromTestCase(TestNotificationService))
    suite.addTests(loader.loadTestsFromTestCase(TestServiceIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestServiceErrorHandling))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)