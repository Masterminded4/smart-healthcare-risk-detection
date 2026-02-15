# Healthcare Risk Detection API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently no authentication required. In production, implement JWT tokens.

## Endpoints

### Health Assessment

#### POST /health/assess
Assess health risk based on user inputs.

**Request Body:**
```json
{
  "age": 45,
  "heart_rate": 78,
  "blood_pressure_systolic": 125,
  "blood_pressure_diastolic": 82,
  "bmi": 26.5,
  "symptoms": ["chest pain", "shortness of breath"],
  "smoking": false,
  "exercise_frequency": 2,
  "family_history": ["hypertension", "diabetes"],
  "latitude": 40.7128,
  "longitude": -74.0060,
  "user_id": "user123" (optional)
}
```

**Response (200 OK):**
```json
{
  "overall_risk_level": "HIGH",
  "primary_concern": "Cardiovascular Disease",
  "risk_scores": {
    "Cardiovascular Disease": 0.72,
    "Diabetes": 0.45,
    "Stroke Risk": 0.38,
    "Healthy": 0.12
  },
  "high_risk_diseases": ["Cardiovascular Disease"],
  "recommendation": [
    "Consult a cardiologist immediately",
    "Monitor blood pressure daily",
    "Reduce salt and saturated fat intake"
  ],
  "timestamp": "2026-02-14T10:30:00Z",
  "health_inputs": { ... }
}
```

#### GET /health/history/{user_id}
Get assessment history for a user.

**Response (200 OK):**
```json
{
  "assessments": [
    { ... assessment object ... },
    { ... assessment object ... }
  ]
}
```

#### POST /health/validate
Validate health data without storing.

**Request Body:**
```json
{
  "age": 45,
  "heart_rate": 78,
  ...
}
```

**Response (200 OK):**
```json
{
  "valid": true,
  "errors": []
}
```

### Hospital Finder

#### POST /hospitals/nearby
Find nearby hospitals based on location.

**Request Body:**
```json
{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "radius_km": 15,
  "specialty": "cardiology" (optional),
  "urgency": "high|medium|low"
}
```

**Response (200 OK):**
```json
{
  "hospitals": [
    {
      "id": 1,
      "name": "Central Medical Hospital",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "address": "123 Main St, New York, NY",
      "phone": "+1-212-555-1234",
      "specialties": ["Cardiology", "Emergency"],
      "has_icu": true,
      "rating": 4.8,
      "distance": 0.5,
      "availability": "24/7"
    }
  ],
  "count": 3,
  "location": {
    "latitude": 40.7128,
    "longitude": -74.0060
  }
}
```

#### POST /hospitals/emergency
Get nearest emergency hospitals.

**Request Body:**
```json
{
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

**Response (200 OK):**
```json
{
  "emergency_hospitals": [ ... ]
}
```

### Recommendations

#### POST /recommendations/precautions
Get personalized health precautions.

**Request Body:**
```json
{
  "risk_diseases": ["Hypertension", "Diabetes"],
  "age": 45,
  "lifestyle": "sedentary",
  "conditions": ["overweight"],
  "urgency": "high"
}
```

**Response (200 OK):**
```json
{
  "precautions": {
    "immediate_actions": [
      "Check blood pressure immediately",
      "Get blood glucose test"
    ],
    "short_term_changes": [
      "Start with 15 minutes of walking daily"
    ],
    "long_term_lifestyle": [
      "Aim for 150 minutes moderate exercise per week"
    ],
    "monitoring": [
      "Weekly blood pressure checks"
    ],
    "specialist_referrals": ["Cardiologist", "Endocrinologist"]
  },
  "urgency": "high"
}
```

#### GET /recommendations/lifestyle
Get general lifestyle improvement tips.

**Response (200 OK):**
```json
{
  "tips": {
    "nutrition": [...],
    "exercise": [...],
    "sleep": [...],
    "stress": [...],
    "monitoring": [...]
  }
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid data",
  "details": [
    "Age must be between 1 and 150",
    "Heart rate must be between 30 and 200 bpm"
  ]
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Rate Limiting
Not currently implemented. Add in production:
- 100 requests per minute per IP
- 1000 requests per hour per user

## Status Codes
- `200` - Success
- `400` - Bad Request
- `404` - Not Found
- `500` - Server Error

## Risk Levels
- **CRITICAL**: Risk score > 0.7 (Immediate medical attention required)
- **HIGH**: Risk score 0.5-0.7 (Consult healthcare provider soon)
- **MODERATE**: Risk score 0.3-0.5 (Monitor condition, schedule check-up)
- **LOW**: Risk score < 0.3 (Maintain healthy lifestyle)