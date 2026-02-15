import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Health Assessment Endpoints
export const healthAPI = {
  assess: (healthData) =>
    api.post('/health/assess', healthData),
  
  getHistory: (userId) =>
    api.get(`/health/history/${userId}`),
  
  validate: (healthData) =>
    api.post('/health/validate', healthData)
};

// Hospital Finder Endpoints
export const hospitalsAPI = {
  findNearby: (location, options = {}) =>
    api.post('/hospitals/nearby', {
      latitude: location.latitude,
      longitude: location.longitude,
      ...options
    }),
  
  findEmergency: (location) =>
    api.post('/hospitals/emergency', {
      latitude: location.latitude,
      longitude: location.longitude
    })
};

// Recommendations Endpoints
export const recommendationsAPI = {
  getPrecautions: (data) =>
    api.post('/recommendations/precautions', data),
  
  getLifestyleTips: () =>
    api.get('/recommendations/lifestyle')
};

// Error handler
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.data || error.message);
    throw error;
  }
);

export default api;