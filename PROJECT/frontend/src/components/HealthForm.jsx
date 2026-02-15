import React, { useState } from 'react';
import axios from 'axios';
import './HealthForm.css';

const HealthForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    age: '',
    heart_rate: '',
    blood_pressure_systolic: '',
    blood_pressure_diastolic: '',
    bmi: '',
    symptoms: [],
    smoking: false,
    exercise_frequency: '',
    family_history: [],
    latitude: '',
    longitude: ''
  });

  const [errors, setErrors] = useState([]);
  const [loading, setLoading] = useState(false);

  const symptomOptions = [
    'chest pain',
    'shortness of breath',
    'dizziness',
    'fatigue',
    'headache',
    'nausea',
    'irregular heartbeat'
  ];

  const familyHistoryOptions = [
    'hypertension',
    'diabetes',
    'cardiovascular disease',
    'stroke',
    'cancer',
    'obesity'
  ];

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSymptomChange = (symptom) => {
    setFormData(prev => ({
      ...prev,
      symptoms: prev.symptoms.includes(symptom)
        ? prev.symptoms.filter(s => s !== symptom)
        : [...prev.symptoms, symptom]
    }));
  };

  const handleFamilyHistoryChange = (disease) => {
    setFormData(prev => ({
      ...prev,
      family_history: prev.family_history.includes(disease)
        ? prev.family_history.filter(d => d !== disease)
        : [...prev.family_history, disease]
    }));
  };

  const getCurrentLocation = () => {
    if (navigator.geolocation) {
      setLoading(true);
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setFormData(prev => ({
            ...prev,
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          }));
          setLoading(false);
        },
        (error) => {
          setErrors(['Unable to get location: ' + error.message]);
          setLoading(false);
        }
      );
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrors([]);

    try {
      const response = await axios.post(
        'http://localhost:5000/api/health/assess',
        {
          ...formData,
          age: parseInt(formData.age),
          heart_rate: parseInt(formData.heart_rate),
          blood_pressure_systolic: parseInt(formData.blood_pressure_systolic),
          blood_pressure_diastolic: parseInt(formData.blood_pressure_diastolic),
          bmi: parseFloat(formData.bmi),
          exercise_frequency: parseInt(formData.exercise_frequency),
          latitude: parseFloat(formData.latitude),
          longitude: parseFloat(formData.longitude)
        }
      );

      onSubmit(response.data);
    } catch (error) {
      setErrors([
        error.response?.data?.message || 
        'Error submitting form. Please try again.'
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="health-form-container">
      <h2>Health Risk Assessment</h2>
      
      {errors.length > 0 && (
        <div className="error-messages">
          {errors.map((error, idx) => (
            <p key={idx}>{error}</p>
          ))}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        {/* Basic Vitals */}
        <fieldset>
          <legend>Basic Vitals</legend>
          
          <div className="form-group">
            <label>Age *</label>
            <input
              type="number"
              name="age"
              value={formData.age}
              onChange={handleInputChange}
              required
              min="1"
              max="150"
            />
          </div>

          <div className="form-group">
            <label>Heart Rate (bpm) *</label>
            <input
              type="number"
              name="heart_rate"
              value={formData.heart_rate}
              onChange={handleInputChange}
              required
              min="30"
              max="200"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Systolic BP (mmHg) *</label>
              <input
                type="number"
                name="blood_pressure_systolic"
                value={formData.blood_pressure_systolic}
                onChange={handleInputChange}
                required
                min="50"
                max="300"
              />
            </div>
            <div className="form-group">
              <label>Diastolic BP (mmHg) *</label>
              <input
                type="number"
                name="blood_pressure_diastolic"
                value={formData.blood_pressure_diastolic}
                onChange={handleInputChange}
                required
                min="30"
                max="200"
              />
            </div>
          </div>

          <div className="form-group">
            <label>BMI *</label>
            <input
              type="number"
              name="bmi"
              step="0.1"
              value={formData.bmi}
              onChange={handleInputChange}
              required
              min="10"
              max="60"
            />
          </div>
        </fieldset>

        {/* Symptoms */}
        <fieldset>
          <legend>Current Symptoms</legend>
          <div className="checkbox-group">
            {symptomOptions.map(symptom => (
              <label key={symptom}>
                <input
                  type="checkbox"
                  checked={formData.symptoms.includes(symptom)}
                  onChange={() => handleSymptomChange(symptom)}
                />
                {symptom.charAt(0).toUpperCase() + symptom.slice(1)}
              </label>
            ))}
          </div>
        </fieldset>

        {/* Lifestyle */}
        <fieldset>
          <legend>Lifestyle Factors</legend>
          
          <div className="form-group">
            <label>Exercise Frequency (days/week) *</label>
            <input
              type="number"
              name="exercise_frequency"
              value={formData.exercise_frequency}
              onChange={handleInputChange}
              required
              min="0"
              max="7"
            />
          </div>

          <div className="form-group checkbox">
            <label>
              <input
                type="checkbox"
                name="smoking"
                checked={formData.smoking}
                onChange={handleInputChange}
              />
              I smoke
            </label>
          </div>
        </fieldset>

        {/* Family History */}
        <fieldset>
          <legend>Family Medical History</legend>
          <div className="checkbox-group">
            {familyHistoryOptions.map(disease => (
              <label key={disease}>
                <input
                  type="checkbox"
                  checked={formData.family_history.includes(disease)}
                  onChange={() => handleFamilyHistoryChange(disease)}
                />
                {disease.charAt(0).toUpperCase() + disease.slice(1)}
              </label>
            ))}
          </div>
        </fieldset>

        {/* Location */}
        <fieldset>
          <legend>Location (for hospital finder)</legend>
          <button
            type="button"
            onClick={getCurrentLocation}
            disabled={loading}
          >
            Get Current Location
          </button>
          
          {formData.latitude && formData.longitude && (
            <p>Location: {formData.latitude.toFixed(4)}, {formData.longitude.toFixed(4)}</p>
          )}
        </fieldset>

        <button type="submit" disabled={loading}>
          {loading ? 'Assessing...' : 'Assess My Health'}
        </button>
      </form>
    </div>
  );
};

export default HealthForm;