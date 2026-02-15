from flask import Blueprint, request, jsonify
from services.geolocation_service import GeoLocationService
from utils.logger import setup_logger

bp = Blueprint('hospitals', __name__, url_prefix='/api/hospitals')
logger = setup_logger(__name__)

geo_service = GeoLocationService()

@bp.route('/nearby', methods=['POST'])
def find_nearby_hospitals():
    """
    Find nearby hospitals based on location and urgency.
    
    Request body:
    {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "radius_km": 10,
        "specialty": "cardiology",
        "urgency": "high"
    }
    """
    try:
        data = request.get_json()
        
        if 'latitude' not in data or 'longitude' not in data:
            return jsonify({"error": "Missing location coordinates"}), 400
        
        radius = data.get('radius_km', 15)
        specialty = data.get('specialty', None)
        urgency = data.get('urgency', 'medium')
        
        hospitals = geo_service.find_hospitals(
            latitude=data['latitude'],
            longitude=data['longitude'],
            radius_km=radius,
            specialty=specialty,
            urgency=urgency
        )
        
        logger.info(f"Found {len(hospitals)} hospitals for location")
        return jsonify({
            "hospitals": hospitals,
            "count": len(hospitals),
            "location": {
                "latitude": data['latitude'],
                "longitude": data['longitude']
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error finding hospitals: {str(e)}")
        return jsonify({"error": "Failed to find hospitals"}), 500

@bp.route('/emergency', methods=['POST'])
def get_emergency_hospitals():
    """Get nearest emergency hospitals."""
    try:
        data = request.get_json()
        hospitals = geo_service.find_emergency_hospitals(
            latitude=data['latitude'],
            longitude=data['longitude'],
            count=5
        )
        return jsonify({"emergency_hospitals": hospitals}), 200
    except Exception as e:
        logger.error(f"Error in emergency search: {str(e)}")
        return jsonify({"error": "Emergency search failed"}), 500