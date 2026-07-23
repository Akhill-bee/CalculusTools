# app/main.py
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.solvers.derivatives import differentiate_expression
from app.solvers.implicit import differentiate_implicit
from app.solvers.integrals import integrate_expression
from app.solvers.taylor import calculate_taylor_series

# Calculate absolute path to the templates directory (supports both root/templates and app/templates)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

if not os.path.exists(TEMPLATE_DIR):
    TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR)
CORS(app)

# Initialize Limiter using the client's IP address
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "success": False,
        "error": "Rate limit exceeded. Please slow down and try again shortly!"
    }), 429

@app.route("/")
def index():
    # Safely serve static index.html from TEMPLATE_DIR
    return send_from_directory(TEMPLATE_DIR, 'index.html')

# --- API Endpoints ---

@app.route("/api/derivative", methods=["POST"])
@limiter.limit("10 per minute")
def derivative():
    data = request.get_json() or {}
    return jsonify(differentiate_expression(
        data.get("latex_input", ""), 
        var_str=data.get("variable", "x"), 
        order=data.get("order", 1)
    ))

@app.route("/api/implicit", methods=["POST"])
@limiter.limit("10 per minute")
def implicit():
    data = request.get_json() or {}
    return jsonify(differentiate_implicit(
        data.get("latex_input", ""), 
        x_var=data.get("x_var", "x"), 
        y_var=data.get("y_var", "y")
    ))

@app.route("/api/integral", methods=["POST"])
@limiter.limit("10 per minute")
def integral():
    data = request.get_json() or {}
    return jsonify(integrate_expression(
        data.get("latex_input", ""), 
        var_str=data.get("variable", "x"), 
        lower_bound=data.get("lower_bound", None) or None, 
        upper_bound=data.get("upper_bound", None) or None
    ))

@app.route("/api/taylor", methods=["POST"])
@limiter.limit("10 per minute")
def taylor():
    data = request.get_json() or {}
    try:
        num_terms = int(data.get("num_terms", 5))
    except ValueError:
        num_terms = 5

    return jsonify(calculate_taylor_series(
        data.get("latex_input", ""), 
        var_str=data.get("variable", "x"), 
        center=data.get("center", "0"), 
        num_terms=num_terms
    ))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)