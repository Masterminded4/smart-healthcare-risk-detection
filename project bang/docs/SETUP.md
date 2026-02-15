# Setup & Installation Guide

## Prerequisites

- Python 3.8+
- Node.js 14+
- Docker & Docker Compose (for containerized setup)
- Git
- 2GB RAM minimum
- 500MB free disk space

## Local Development Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/Masterminded4/smart-healthcare-risk-detection.git
cd smart-healthcare-risk-detection
```

### Step 2: Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp ../.env.example .env
# Edit .env with your settings

# Run development server
python app.py
```

**Backend will run on:** `http://localhost:5000`

### Step 3: Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:5000" > .env

# Start development server
npm start
```

**Frontend will run on:** `http://localhost:3000`

### Step 4: Train ML Model

```bash
cd backend/models

# Generate training data
python generate_training_data.py

# Train model
python train_model.py
```

This creates:
- `disease_model.pkl` - Trained model
- `scaler.pkl` - Feature scaler
- `feature_metadata.json` - Feature information

## Docker Setup

### Using Docker Compose

```bash
# Build and start containers
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop containers
docker-compose down
```

### Access Services
- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- API Docs: http://localhost:5000/api/docs
- Database: localhost:5432

### Database Initialization

```bash
# Enter PostgreSQL container
docker-compose exec database psql -U healthcare -d healthcare_db

# Create tables
\d  # List tables
\q  # Exit
```

## Environment Configuration

### Backend .env

```env
# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://healthcare:password@localhost:5432/healthcare_db

# Email
ENABLE_NOTIFICATIONS=False
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Features
HOSPITAL_SEARCH_RADIUS=15
MODEL_PATH=models/disease_model.pkl
SCALER_PATH=models/scaler.pkl
```

### Frontend .env

```env
REACT_APP_API_URL=http://localhost:5000
```

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_models.py -v

# Run with coverage
pytest --cov=. tests/
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

## Troubleshooting

### Backend Issues

**Port 5000 already in use:**
```bash
lsof -i :5000
kill -9 <PID>
```

**Module not found:**
```bash
pip install -r requirements.txt --upgrade
```

**Model file not found:**
```bash
cd backend/models
python train_model.py
```

### Frontend Issues

**Port 3000 already in use:**
```bash
PORT=3001 npm start
```

**Dependencies conflict:**
```bash
rm -rf node_modules package-lock.json
npm install
```

### Database Issues

**Cannot connect to database:**
```bash
# Check if database is running
docker-compose ps

# Restart database
docker-compose restart database

# Check connection
psql -U healthcare -h localhost -d healthcare_db
```

## Database Backup & Restore

### Backup

```bash
docker-compose exec database pg_dump -U healthcare healthcare_db > backup.sql
```

### Restore

```bash
docker-compose exec -T database psql -U healthcare healthcare_db < backup.sql
```

## Production Deployment

### Using Gunicorn

```bash
cd backend

# Install gunicorn
pip install gunicorn

# Run production server
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

```bash
# Build image
docker build -t healthcare-backend:1.0 ./backend

# Run container
docker run -p 5000:5000 healthcare-backend:1.0
```

### Nginx Configuration

```nginx
upstream backend {
    server localhost:5000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
    }

    location / {
        proxy_pass http://frontend:3000;
    }
}
```

## Performance Optimization

### Backend
- Enable Redis caching
- Use connection pooling
- Optimize database queries
- Add API rate limiting

### Frontend
- Enable production build
- Use code splitting
- Optimize images
- Enable gzip compression

## Monitoring

### Logs Location
- Backend: `backend/logs/app.log`
- Frontend: Browser console
- Database: Docker logs

### Health Check

```bash
curl http://localhost:5000/health
```

Response:
```json
{"status": "healthy", "version": "1.0.0"}
```