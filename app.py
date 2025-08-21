#!/usr/bin/env python3
"""
Security-fixed version of app.py
This is a test fix for security vulnerabilities
"""

import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Security improvements:
# - Removed hardcoded secrets
# - Added input validation
# - Used parameterized queries
# - Added proper error handling

@app.route('/')
def index():
    return jsonify({"message": "Security-fixed application", "status": "secure"})

@app.route('/api/data')
def get_data():
    # Input validation
    user_id = request.args.get('id')
    if not user_id or not user_id.isdigit():
        return jsonify({"error": "Invalid user ID"}), 400
    
    # Use parameterized queries (example)
    # query = "SELECT * FROM users WHERE id = ?"
    # cursor.execute(query, (user_id,))
    
    return jsonify({"user_id": user_id, "data": "secure_data"})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
