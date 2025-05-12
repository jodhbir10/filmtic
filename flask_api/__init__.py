from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import HTTPException
import os
import django
import logging
from django.db import connections
from django.db.utils import OperationalError

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_review.settings')
django.setup()

# Check database connection
try:
    connections['default'].cursor()
    logging.info("Database connection successful.")
except OperationalError as e:
    logging.error(f"Database connection failed: {e}")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": os.environ.get('CORS_ORIGIN', '*')}})  # Dynamic CORS origin
api = Api(app)

# Configure JWT
if 'JWT_SECRET_KEY' not in os.environ:
    raise EnvironmentError("JWT_SECRET_KEY environment variable is not set.")
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
jwt = JWTManager(app)

# Set up rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    headers_enabled=True  # Enable headers for proxies
)
limiter.init_app(app)

# Set up logging
if os.environ.get('FLASK_ENV') == 'development':
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

# Global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return jsonify({"error": e.description}), e.code
    logging.error(f"Unhandled exception: {e}")
    return jsonify({"error": "An unexpected error occurred"}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
@limiter.limit("10 per minute")
def health_check():
    try:
        connections['default'].cursor()
        db_status = "connected"
    except OperationalError:
        db_status = "disconnected"
    return jsonify({"status": "OK", "database": db_status}), 200

# Import routes after app creation to avoid circular imports
from flask_api.routes import ReviewResource, AuthResource, RegisterResource

# Register API endpoints
api.add_resource(ReviewResource, '/api/reviews/', '/api/reviews/<int:review_id>/')
api.add_resource(AuthResource, '/api/auth/login/')
api.add_resource(RegisterResource, '/api/auth/register/')