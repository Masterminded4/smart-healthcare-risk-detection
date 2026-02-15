import React from 'react';
import './RiskDashboard.css';

const RiskDashboard = ({ assessment }) => {
  if (!assessment) return null;

  const getRiskColor = (level) => {
    switch (level) {
      case 'CRITICAL':
        return '#dc3545';
      case 'HIGH':
        return '#ff6b6b';
      case 'MODERATE':
        return '#ffc107';
      case 'LOW':
        return '#28a745';
      default:
        return '#6c757d';
    }
  };

  const getRiskEmoji = (level) => {
    switch (level) {
      case 'CRITICAL':
        return '🚨';
      case 'HIGH':
        return '⚠️';
      case 'MODERATE':
        return '⚡';
      case 'LOW':
        return '✅';
      default:
        return '❓';
    }
  };

  return (
    <div className="dashboard-container">
      <h2>Your Health Assessment Results</h2>

      {/* Risk Level Card */}
      <div className="risk-card" style={{ borderColor: getRiskColor(assessment.overall_risk_level) }}>
        <div className="risk-level-display">
          <span className="risk-emoji">{getRiskEmoji(assessment.overall_risk_level)}</span>
          <span className="risk-level" style={{ color: getRiskColor(assessment.overall_risk_level) }}>
            {assessment.overall_risk_level}
          </span>
        </div>
        <p>Overall Risk Level</p>
      </div>

      {/* Primary Concern */}
      <div className="concern-card">
        <h3>Primary Health Concern</h3>
        <p className="concern-name">{assessment.primary_concern}</p>
        <p className="concern-score">
          Risk Score: {(assessment.risk_scores[assessment.primary_concern] * 100).toFixed(1)}%
        </p>
      </div>

      {/* Risk Scores */}
      <div className="scores-card">
        <h3>Disease Risk Assessment</h3>
        <div className="score-list">
          {Object.entries(assessment.risk_scores).map(([disease, score]) => (
            <div key={disease} className="score-item">
              <span className="disease-name">{disease}</span>
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{
                    width: `${score * 100}%`,
                    backgroundColor: getRiskColor(
                      score > 0.7 ? 'CRITICAL' : 
                      score > 0.5 ? 'HIGH' : 
                      score > 0.3 ? 'MODERATE' : 'LOW'
                    )
                  }}
                />
              </div>
              <span className="score-percent">{(score * 100).toFixed(1)}%</span>
            </div>
          ))}
        </div>
      </div>

      {/* High Risk Diseases */}
      {assessment.high_risk_diseases.length > 0 && (
        <div className="alert-card alert-high">
          <h3>⚠️ Conditions Requiring Attention</h3>
          <ul>
            {assessment.high_risk_diseases.map(disease => (
              <li key={disease}>{disease}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommendations */}
      {assessment.recommendation && (
        <div className="recommendations-card">
          <h3>Recommended Actions</h3>
          {Array.isArray(assessment.recommendation) ? (
            <ul>
              {assessment.recommendation.map((rec, idx) => (
                <li key={idx}>{rec}</li>
              ))}
            </ul>
          ) : (
            <p>{assessment.recommendation}</p>
          )}
        </div>
      )}

      {/* Timestamp */}
      <div className="timestamp">
        Assessment Date: {new Date(assessment.timestamp).toLocaleString()}
      </div>
    </div>
  );
};

export default RiskDashboard;