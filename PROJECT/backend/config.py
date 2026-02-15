import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = os.getenv('FLASK_DEBUG', True)
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    # API Configuration
    API_TITLE = 'Healthcare Risk Detection API'
    API_VERSION = '1.0.0'
    
    # Database (optional, for storing assessments)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///healthcare.db'
    )
    
    # Geolocation
    GEOLOCATION_API_KEY = os.getenv('GEOLOCATION_API_KEY')
    
    # Email notifications
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = os.getenv('SMTP_PORT', 587)
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    
    # Model paths
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/disease_model.pkl')
    SCALER_PATH = os.getenv('SCALER_PATH', 'models/scaler.pkl')

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'