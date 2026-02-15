import React from 'react';
import './PrecautionsList.css';

const PrecautionsList = ({ diseases, recommendations }) => {
  return (
    <div className="precautions-container">
      <h2>💊 Health Precautions & Recommendations</h2>

      {diseases && diseases.length > 0 && (
        <div className="diseases-section">
          <h3>Conditions Identified</h3>
          <ul className="disease-list">
            {diseases.map((disease, idx) => (
              <li key={idx} className="disease-item">
                {disease}
              </li>
            ))}
          </ul>
        </div>
      )}

      {recommendations && recommendations.length > 0 && (
        <div className="recommendations-section">
          <h3>Immediate Actions</h3>
          <ul className="recommendation-list">
            {recommendations.map((rec, idx) => (
              <li key={idx} className="recommendation-item">
                ✓ {rec}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="general-precautions">
        <h3>General Health Tips</h3>
        <div className="tips-grid">
          <div className="tip-card">
            <h4>🏃 Exercise</h4>
            <p>Aim for 150 minutes of moderate activity weekly</p>
          </div>
          <div className="tip-card">
            <h4>🥗 Nutrition</h4>
            <p>Eat balanced diet with fruits and vegetables</p>
          </div>
          <div className="tip-card">
            <h4>😴 Sleep</h4>
            <p>Maintain 7-9 hours of quality sleep daily</p>
          </div>
          <div className="tip-card">
            <h4>🧘 Stress</h4>
            <p>Practice meditation or relaxation techniques</p>
          </div>
        </div>
      </div>

      <div className="important-notice">
        <p>
          <strong>⚠️ Important:</strong> This assessment is for informational purposes only.
          Please consult with healthcare professionals for proper diagnosis and treatment.
        </p>
      </div>
    </div>
  );
};

export default PrecautionsList;