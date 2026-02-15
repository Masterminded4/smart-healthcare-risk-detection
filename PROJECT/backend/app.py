from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from routes import health_assessment, hospital_finder, recommendations
from utils.logger import setup_logger
import traceback

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Setup logging
logger = setup_logger(__name__)

# Register blueprints
app.register_blueprint(health_assessment.bp)
app.register_blueprint(hospital_finder.bp)
app.register_blueprint(recommendations.bp)

@app.errorhandler(400)
def bad_request(error):
    logger.warning(f"Bad request: {error}")
    return jsonify({"error": "Bad request", "message": str(error)}), 400

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}\n{traceback.format_exc()}")
    return jsonify({"error": "Internal server error"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "version": "1.0.0"}), 200

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)