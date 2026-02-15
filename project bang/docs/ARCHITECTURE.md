# System Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Layer                            │
│  (React Frontend - HealthForm, Dashboard, HospitalLocator)   │
└─────────────────┬───────────────────────────────────────────┘
                  │ HTTPS/REST API
                  ↓
┌─────────────────────────────────────────────────────────────┐
│                    API Layer (Flask)                         │
│  ├── /api/health/assess                                      │
│  ├── /api/hospitals/nearby                                   │
│  └── /api/recommendations/precautions                        │
└─────────────────┬───────────────────────────────────────────┘
                  │
        ┌─────────┼─────────┐
        ↓         ↓         ↓
  ┌──────────┐ ┌──────────┐ ┌──────────────┐
  │ Prediction│ │Geolocation│ │Recommendation│
  │ Service   │ │ Service  │ │ Service      │
  └──────┬───┘ └────┬─────┘ └──────┬───────┘
         │          │              │
         ↓          ↓              ↓
  ┌──────────┐ ┌──────────┐ ┌──────────────┐
  │ ML Model │ │Hospital  │ │Health Tips   │
  │(sklearn) │ │Database  │ │Database      │
  └──────────┘ └──────────┘ └──────────────┘
         │
         ↓
  ┌──────────────────┐
  │ PostgreSQL DB    │
  │ (User History)   │
  └──────────────────┘
```

## Component Architecture

### Frontend (React)
- **HealthForm.jsx**: Input form for health data
- **RiskDashboard.jsx**: Display risk assessment results
- **HospitalLocator.jsx**: Find nearby hospitals
- **PrecautionsList.jsx**: Display recommendations
- **api.js**: API service layer

### Backend (Flask)

#### Routes
- `health_assessment.py`: Health assessment endpoints
- `hospital_finder.py`: Hospital location endpoints
- `recommendations.py`: Health recommendation endpoints

#### Services
- `prediction_service.py`: Orchestrates ML predictions
- `geolocation_service.py`: Finds nearby hospitals
- `notification_service.py`: Sends alerts/notifications

#### Models
- `risk_predictor.py`: ML model wrapper
- `disease_model.pkl`: Trained Random Forest model
- `scaler.pkl`: Feature scaling object

#### Utils
- `data_validator.py`: Input validation
- `logger.py`: Logging configuration
- `encryption.py`: Data encryption (optional)

## Data Flow

### Health Assessment Flow
```
1. User fills health form
   ↓
2. Frontend validates data
   ↓
3. POST /api/health/assess
   ↓
4. Backend validates input
   ↓
5. Extract features
   ↓
6. Apply feature scaling
   ↓
7. ML model prediction
   ↓
8. Return risk scores & recommendations
   ↓
9. Store in database (optional)
   ↓
10. Display results to user
```

### Hospital Finding Flow
```
1. User clicks "Find Hospitals"
   ↓
2. Frontend gets location (GPS or manual)
   ↓
3. POST /api/hospitals/nearby
   ↓
4. Backend calculates distances
   ↓
5. Filter by radius & specialty
   ↓
6. Sort by distance & rating
   ↓
7. Return hospital list
   ↓
8. Display on map/list
```

## Technology Stack

### Frontend
- React 18.2
- Axios (HTTP client)
- CSS3 (responsive design)
- Geolocation API

### Backend
- Flask 3.0
- scikit-learn (ML)
- PostgreSQL (database)
- Python 3.8+

### DevOps
- Docker & Docker Compose
- Gunicorn (production server)
- Nginx (reverse proxy - optional)

## Database Schema

### Users Table
```
id (UUID)
name (str)
email (str)
phone (str)
location_lat (float)
location_lon (float)
created_at (timestamp)
```

### Assessments Table
```
id (UUID)
user_id (FK)
age (int)
heart_rate (int)
blood_pressure_systolic (int)
blood_pressure_diastolic (int)
bmi (float)
symptoms (JSON)
family_history (JSON)
risk_level (str)
risk_scores (JSON)
recommendations (JSON)
created_at (timestamp)
```

## ML Model Pipeline

### Training Pipeline
```
Raw Data
   ↓
Data Cleaning
   ↓
Feature Extraction
   ↓
Feature Scaling (StandardScaler)
   ↓
Train/Test Split (80/20)
   ↓
Model Training (Random Forest)
   ↓
Model Evaluation
   ↓
Save model.pkl & scaler.pkl
```

### Prediction Pipeline
```
Health Input
   ↓
Validate Input
   ↓
Extract Features
   ↓
Load Scaler
   ↓
Scale Features
   ↓
Load Model
   ↓
Predict Probability
   ↓
Generate Recommendations
   ↓
Return Results
```

## Scalability Considerations

### Horizontal Scaling
- Use load balancer (Nginx/HAProxy)
- Multiple Flask instances
- Database replication

### Caching
- Redis for hospital data
- Cache ML model in memory
- API response caching

### Optimization
- Async task processing (Celery)
- Database indexing
- API rate limiting

## Security Measures

1. **Input Validation**: All inputs validated server-side
2. **Data Encryption**: HTTPS for transit, encryption at rest
3. **Authentication**: JWT tokens (future)
4. **Authorization**: Role-based access control
5. **Audit Logging**: Track all assessments
6. **HIPAA Compliance**: Secure data handling

## Monitoring & Logging

- Application logs: `logs/app.log`
- Error tracking: Sentry (optional)
- Performance monitoring: New Relic (optional)
- Health checks: `/health` endpoint