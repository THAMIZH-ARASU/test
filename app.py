import sqlite3
import flask
from flask import request, redirect, jsonify
import os
import logging
import json
import base64
import hmac
import hashlib

app = flask.Flask(__name__)

# Environment variables for secrets
API_KEY = os.environ.get('API_KEY')

# Authentication helpers
def is_authenticated(request):
    # Simple placeholder for authentication check
    return 'Authenticated' in request.headers

def is_admin(request):
    # Simple placeholder for admin check
    return 'Admin' in request.headers

# Fixed SQL injection vulnerability
def fixed_sql_injection(username):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    data = cursor.fetchall()
    conn.close()
    return data

# Fixed broken access control
@app.route('/admin_dashboard')
def fixed_access_control():
    if not is_admin(request):
        return "Access denied", 403
    return "Welcome to the Admin Dashboard!"

# Fixed hardcoded secrets
def fixed_hardcoded_secrets():
    print(f"Using API key from environment variable: {API_KEY}")

# Fixed cross-site scripting (XSS)
@app.route('/xss_page')
def fixed_xss():
    user_input = request.args.get('name', 'Guest')
    return f"Hello, {flask.escape(user_input)}!"

# Fixed insufficient logging and monitoring
def fixed_no_logging(amount, user_id):
    logging.info(f"Processing payment for user {user_id} with amount {amount}")
    if amount > 1000:
        logging.warning(f"Large payment detected for user {user_id} with amount {amount}")
    return "Payment processed."

# Fixed insecure deserialization
def fixed_insecure_deserialization(encoded_data):
    data = base64.b64decode(encoded_data)
    return json.loads(data)

# Fixed invalid redirects and forwards
@app.route('/redirect')
def fixed_redirect():
    url = request.args.get('url')
    if not url.startswith('/'):
        return "Invalid redirect URL", 400
    return redirect(url)

if __name__ == '__main__':
    app.run()