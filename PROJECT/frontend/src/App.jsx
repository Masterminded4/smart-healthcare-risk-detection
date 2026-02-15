import React, { useState } from 'react';
import HealthForm from './components/HealthForm';
import RiskDashboard from './components/RiskDashboard';
import HospitalLocator from './components/HospitalLocator';
import PrecautionsList from './components/PrecautionsList';
import './App.css';

function App() {
  const [assessment, setAssessment] = useState(null);
  const [location, setLocation] = useState(null);

  const handleHealthFormSubmit = (data) => {
    setAssessment(data);
    if (data.health_inputs) {
      setLocation({
        latitude: data.health_inputs.latitude,
        longitude: data.health_inputs.longitude
      });
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🏥 Smart Healthcare Risk Detection</h1>
        <p>Early Risk Detection & Hospital Finder</p>
      </header>

      <main className="app-main">
        {!assessment ? (
          <HealthForm onSubmit={handleHealthFormSubmit} />
        ) : (
          <div className="results-container">
            <RiskDashboard assessment={assessment} />
            
            {location && (
              <>
                <HospitalLocator
                  latitude={location.latitude}
                  longitude={location.longitude}
                  riskLevel={assessment.overall_risk_level}
                />
                <PrecautionsList
                  diseases={assessment.high_risk_diseases}
                  recommendations={assessment.recommendation}
                />
              </>
            )}
            
            <button
              className="btn-new-assessment"
              onClick={() => {
                setAssessment(null);
                setLocation(null);
              }}
            >
              ← New Assessment
            </button>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>⚠️ Disclaimer: This system is for informational purposes only and should not replace professional medical advice.</p>
      </footer>
    </div>
  );
}

export default App;