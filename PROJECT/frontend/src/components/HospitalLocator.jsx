import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './HospitalLocator.css';

const HospitalLocator = ({ latitude, longitude, riskLevel }) => {
  const [hospitals, setHospitals] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [filterSpecialty, setFilterSpecialty] = useState('');

  useEffect(() => {
    if (latitude && longitude) {
      findHospitals();
    }
  }, [latitude, longitude]);

  const findHospitals = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await axios.post(
        'http://localhost:5000/api/hospitals/nearby',
        {
          latitude: parseFloat(latitude),
          longitude: parseFloat(longitude),
          radius_km: 15,
          specialty: filterSpecialty || null,
          urgency: riskLevel === 'CRITICAL' || riskLevel === 'HIGH' ? 'high' : 'medium'
        }
      );

      setHospitals(response.data.hospitals);
    } catch (err) {
      setError('Failed to find hospitals');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="hospital-locator">
      <h2>Nearby Hospitals & Medical Centers</h2>

      {error && <div className="error-message">{error}</div>}

      <div className="filter-section">
        <input
          type="text"
          placeholder="Filter by specialty..."
          value={filterSpecialty}
          onChange={(e) => setFilterSpecialty(e.target.value)}
        />
        <button onClick={findHospitals} disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      <div className="hospitals-list">
        {hospitals.length === 0 ? (
          <p>No hospitals found in your area</p>
        ) : (
          hospitals.map(hospital => (
            <div key={hospital.id} className="hospital-card">
              <div className="hospital-header">
                <h3>{hospital.name}</h3>
                <span className="distance">{hospital.distance} km away</span>
              </div>

              <div className="hospital-details">
                <p>
                  <strong>Address:</strong> {hospital.address}
                </p>
                <p>
                  <strong>Phone:</strong> {hospital.phone}
                </p>
                <p>
                  <strong>Specialties:</strong> {hospital.specialties.join(', ')}
                </p>
                <p>
                  <strong>Rating:</strong> ⭐ {hospital.rating}/5
                </p>
                {hospital.has_icu && (
                  <p className="icu-badge">🏥 Has ICU</p>
                )}
              </div>

              <button className="call-btn">
                Call Now
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default HospitalLocator;