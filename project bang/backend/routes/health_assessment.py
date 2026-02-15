from flask import Blueprint, request, jsonify
from services.prediction_service import PredictionService
from utils.data_validator import validate_health_data
from utils.logger import setup_logger

bp = Blueprint('health', __name__, url_prefix='/api/health')
logger = setup_logger(__name__)

prediction_service = PredictionService()

@bp.route('/assess', methods=['POST'])
def assess_health():
    """
    Assess health risk based on user inputs.
    
    Request body:
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
    """
    try:
        data = request.get_json()
        
        # Validate input
        is_valid, errors = validate_health_data(data)
        if not is_valid:
            logger.warning(f"Invalid health data: {errors}")
            return jsonify({"error": "Invalid data", "details": errors}), 400
        
        # Get risk assessment
        result = prediction_service.assess_risk(data)
        
        logger.info(f"Health assessment completed - Risk level: {result['overall_risk_level']}")
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in health assessment: {str(e)}")
        return jsonify({"error": "Assessment failed"}), 500

@bp.route('/history/<user_id>', methods=['GET'])
def get_assessment_history(user_id):
    """Get historical assessments for a user."""
    try:
        history = prediction_service.get_user_history(user_id)
        return jsonify({"assessments": history}), 200
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        return jsonify({"error": "Failed to fetch history"}), 500

@bp.route('/validate', methods=['POST'])
def validate_inputs():
    """Validate health data without storing."""
    try:
        data = request.get_json()
        is_valid, errors = validate_health_data(data)
        return jsonify({
            "valid": is_valid,
            "errors": errors if not is_valid else []
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400