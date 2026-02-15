from flask import Blueprint, request, jsonify
from services.prediction_service import PredictionService
from utils.logger import setup_logger

bp = Blueprint('recommendations', __name__, url_prefix='/api/recommendations')
logger = setup_logger(__name__)

prediction_service = PredictionService()

@bp.route('/precautions', methods=['POST'])
def get_precautions():
    """
    Get personalized health precautions.
    
    Request body:
    {
        "risk_diseases": ["Hypertension", "Diabetes"],
        "age": 45,
        "lifestyle": "sedentary",
        "conditions": ["overweight"]
    }
    """
    try:
        data = request.get_json()
        
        precautions = prediction_service.generate_precautions(
            diseases=data.get('risk_diseases', []),
            age=data.get('age'),
            lifestyle=data.get('lifestyle'),
            conditions=data.get('conditions', [])
        )
        
        return jsonify({
            "precautions": precautions,
            "urgency": data.get('urgency', 'normal')
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating precautions: {str(e)}")
        return jsonify({"error": "Failed to generate precautions"}), 500

@bp.route('/lifestyle', methods=['GET'])
def get_lifestyle_tips():
    """Get general lifestyle improvement tips."""
    try:
        tips = prediction_service.get_lifestyle_tips()
        return jsonify({"tips": tips}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500