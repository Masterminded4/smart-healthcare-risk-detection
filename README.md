# Smart Healthcare Early Risk Detection System

An AI-powered system that analyzes health inputs and predicts early disease risks, with hospital locator and personalized recommendations.

## 🎯 Features

- **Health Risk Assessment**: Analyzes heart rate, symptoms, lifestyle, and medical history
- **AI Disease Prediction**: Uses machine learning to predict cardiovascular disease, diabetes, and stroke risk
- **Hospital Finder**: Locates nearby hospitals based on location and urgency
- **Personalized Recommendations**: Generates health precautions and lifestyle tips
- **Location Services**: Integrates GPS for finding nearest medical facilities
- **User History**: Tracks assessment history over time

## 🛠️ Tech Stack

**Backend:**
- Flask (Python web framework)
- scikit-learn (ML model)
- geopy (Geolocation)
- PostgreSQL (Database)

**Frontend:**
- React.js
- Axios (HTTP client)
- CSS3

**Deployment:**
- Docker & Docker Compose
- Gunicorn (Production server)

## 📋 Requirements

- Python 3.8+
- Node.js 14+
- Docker & Docker Compose
- Git

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/Masterminded4/smart-healthcare-risk-detection.git
cd smart-healthcare-risk-detection
```

### 2. Setup Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Run with Docker
```bash
docker-compose up -d
```

### 4. Access Application
- Frontend: http://localhost:3000
- API: http://localhost:5000
- API Docs: http://localhost:5000/api/docs

## 📖 API Endpoints

### Health Assessment
- `POST /api/health/assess` - Assess health risk
- `GET /api/health/history/<user_id>` - Get assessment history
- `POST /api/health/validate` - Validate health data

### Hospital Finder
- `POST /api/hospitals/nearby` - Find nearby hospitals
- `POST /api/hospitals/emergency` - Find emergency hospitals

### Recommendations
- `POST /api/recommendations/precautions` - Get precautions
- `GET /api/recommendations/lifestyle` - Get lifestyle tips

## 🧠 Machine Learning Model

The system uses a Random Forest Classifier trained on:
- Demographics (age, gender)
- Vital signs (heart rate, blood pressure, BMI)
- Symptoms
- Lifestyle factors
- Family history

### Training Data
```python
Features: [age, HR, BP_systolic, BP_diastolic, BMI, exercise, smoking, symptoms_count, family_history_count]
Target: [Cardiovascular Disease, Diabetes, Stroke Risk, Healthy]
```

## 🔒 Privacy & Security

- End-to-end encryption for sensitive data
- HIPAA compliance standards
- No personal data storage without consent
- Secure API authentication
- Data anonymization in logs

## 📊 Sample Assessment Request

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
  "longitude": -74.0060
}
```

## 📈 Response Example

```json
{
  "overall_risk_level": "HIGH",
  "primary_concern": "Cardiovascular Disease",
  "risk_scores": {
    "Cardiovascular Disease": 0.72,
    "Diabetes": 0.45,
    "Stroke Risk": 0.38
  },
  "high_risk_diseases": ["Cardiovascular Disease"],
  "recommendation": [
    "Consult a cardiologist immediately",
    "Monitor blood pressure daily"
  ],
  "timestamp": "2026-02-13T10:30:00Z"
}
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

MIT License - see LICENSE file for details

## ⚠️ Disclaimer

This system is for informational purposes only and should not be used as a substitute for professional medical advice. Always consult with qualified healthcare providers for diagnosis and treatment.

## 📧 Support

For issues and questions, please open an issue on GitHub.

## 🎓 Learn More

- [Model Training Guide](docs/MODEL_TRAINING.md)
- [API Documentation](docs/API.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
- [Setup Instructions](docs/SETUP.md)n
