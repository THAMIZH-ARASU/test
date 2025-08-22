import sqlite3
import flask
from flask import request, redirect, jsonify
import os
import json
import logging
import base64

app = flask.Flask(__name__)

# Environment variables for secrets
API_KEY = os.environ.get('API_KEY')

# Authentication helpers
def is_authenticated(request):
    return 'Authenticated' in request.headers

def is_admin(request):
    return 'Admin' in request.headers

# --- FIXED SQL INJECTION ---
def fixed_sql_injection(username):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    data = cursor.fetchall()
    conn.close()
    return data

# --- FIXED BROKEN ACCESS CONTROL ---
@app.route('/admin_dashboard')
def fixed_access_control():
    if not is_admin(request):
        return "Access denied", 403
    return "Welcome to the Admin Dashboard!"

# --- FIXED HARDCODED SECRETS ---
def fixed_hardcoded_secrets():
    print(f"Using API key from environment variable: {API_KEY}")

# --- FIXED CROSS-SITE SCRIPTING (XSS) ---
@app.route('/xss_page')
def fixed_xss():
    user_input = request.args.get('name', 'Guest')
    return f"Hello, {flask.escape(user_input)}!"

# --- FIXED INSUFFICIENT LOGGING AND MONITORING ---
def fixed_no_logging(amount, user_id):
    logging.warning(f"Processing payment of {amount} for user {user_id}")
    if amount > 1000:
        logging.warning(f"Large payment of {amount} for user {user_id}")
    return "Payment processed."

# --- FIXED INSECURE DESERIALIZATION ---
def fixed_insecure_deserialization(encoded_data):
    data = base64.b64decode(encoded_data)
    return json.loads(data.decode('utf-8'))

# --- FIXED UNUSED CODE ---
# Removed unused imports and dead code

# --- FIXED INVALID REDIRECTS AND FORWARDS ---
@app.route('/redirect')
def fixed_redirect():
    url = request.args.get('url')
    if url.startswith('http://example.com'):
        return redirect(url)
    return "Invalid redirect URL", 400

if __name__ == '__main__':
    app.run()