from geopy.distance import geodesic
from haversine import haversine, Unit
from utils.logger import setup_logger
import requests

logger = setup_logger(__name__)

class GeoLocationService:
    def __init__(self):
        # Sample hospital database - in production use real API
        self.hospitals = [
            {
                "id": 1,
                "name": "Central Medical Hospital",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "address": "123 Main St, New York, NY",
                "phone": "+1-212-555-1234",
                "specialties": ["Cardiology", "Neurology", "Emergency"],
                "has_icu": True,
                "rating": 4.8,
                "distance": None
            },
            {
                "id": 2,
                "name": "City Health Center",
                "latitude": 40.7185,
                "longitude": -74.0060,
                "address": "456 Park Ave, New York, NY",
                "phone": "+1-212-555-5678",
                "specialties": ["General Practice", "Cardiology"],
                "has_icu": False,
                "rating": 4.5,
                "distance": None
            },
            {
                "id": 3,
                "name": "Emergency Care Clinic",
                "latitude": 40.7050,
                "longitude": -74.0080,
                "address": "789 Broadway, New York, NY",
                "phone": "+1-212-555-9999",
                "specialties": ["Emergency", "Trauma", "Cardiology"],
                "has_icu": True,
                "rating": 4.6,
                "distance": None
            }
        ]
    
    def find_hospitals(self, latitude, longitude, radius_km=15, 
                       specialty=None, urgency='medium'):
        """Find hospitals within radius."""
        user_location = (latitude, longitude)
        nearby = []
        
        for hospital in self.hospitals:
            hospital_location = (hospital['latitude'], hospital['longitude'])
            distance = haversine(user_location, hospital_location, unit=Unit.KILOMETERS)
            
            if distance <= radius_km:
                hospital_copy = hospital.copy()
                hospital_copy['distance'] = round(distance, 2)
                
                # Filter by specialty if provided
                if specialty:
                    if specialty.lower() in [s.lower() for s in hospital['specialties']]:
                        nearby.append(hospital_copy)
                else:
                    nearby.append(hospital_copy)
        
        # Sort by distance and rating
        nearby.sort(key=lambda x: (x['distance'], -x['rating']))
        
        # For emergencies, prioritize hospitals with ICU
        if urgency == 'high':
            nearby.sort(key=lambda x: (-x['has_icu'], x['distance']))
        
        return nearby[:10]  # Return top 10
    
    def find_emergency_hospitals(self, latitude, longitude, count=5):
        """Find nearest emergency hospitals."""
        user_location = (latitude, longitude)
        emergency_hospitals = []
        
        for hospital in self.hospitals:
            if 'Emergency' in hospital['specialties']:
                hospital_location = (hospital['latitude'], hospital['longitude'])
                distance = haversine(user_location, hospital_location, unit=Unit.KILOMETERS)
                
                hospital_copy = hospital.copy()
                hospital_copy['distance'] = round(distance, 2)
                emergency_hospitals.append(hospital_copy)
        
        # Sort by distance
        emergency_hospitals.sort(key=lambda x: x['distance'])
        
        return emergency_hospitals[:count]
    
    def get_hospital_details(self, hospital_id):
        """Get detailed information about a hospital."""
        for hospital in self.hospitals:
            if hospital['id'] == hospital_id:
                return hospital
        return None