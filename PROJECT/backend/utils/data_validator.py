def validate_health_data(data):
    """Validate health assessment data."""
    errors = []
    
    # Required fields
    required = ['age', 'heart_rate', 'blood_pressure_systolic', 
                'blood_pressure_diastolic', 'bmi']
    
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Validate ranges
    if 'age' in data:
        if not (0 < data['age'] < 150):
            errors.append("Age must be between 0 and 150")
    
    if 'heart_rate' in data:
        if not (30 < data['heart_rate'] < 200):
            errors.append("Heart rate must be between 30 and 200 bpm")
    
    if 'blood_pressure_systolic' in data:
        if not (50 < data['blood_pressure_systolic'] < 300):
            errors.append("Systolic BP must be between 50 and 300 mmHg")
    
    if 'blood_pressure_diastolic' in data:
        if not (30 < data['blood_pressure_diastolic'] < 200):
            errors.append("Diastolic BP must be between 30 and 200 mmHg")
    
    if 'bmi' in data:
        if not (10 < data['bmi'] < 60):
            errors.append("BMI must be between 10 and 60")
    
    if 'exercise_frequency' in data:
        if not (0 <= data['exercise_frequency'] <= 7):
            errors.append("Exercise frequency must be 0-7 days per week")
    
    return (len(errors) == 0, errors)