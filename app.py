import sqlite3
import flask
from flask import request, redirect, jsonify
import os
import base64
import json
import logging

# Define minimal authentication helpers
def is_authenticated(request):
    return 'Authenticated' in request.headers

def is_admin(request):
    return 'Admin' in request.headers

# --- FIXED VULNERABILITY 1: SQL INJECTION ---
def fetch_user(username):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    data = cursor.fetchall()
    conn.close()
    return data

# --- FIXED VULNERABILITY 2: BROKEN ACCESS CONTROL ---
app = flask.Flask(__name__)
@app.route('/admin_dashboard')
def access_control():
    if not is_admin(request):
        return "Access denied", 403
    logging.info("Admin dashboard accessed")
    return "Welcome to the Admin Dashboard!"

# --- FIXED VULNERABILITY 3: HARDCODED SECRETS ---
API_KEY = os.environ.get('API_KEY')
def print_secrets():
    print(f"Using API key from environment: {API_KEY}")

# --- FIXED VULNERABILITY 5: CROSS-SITE SCRIPTING (XSS) ---
@app.route('/xss_page')
def render_ui():
    user_input = request.args.get('name', 'Guest')
    return f"Hello, {flask.escape(user_input)}!"

# --- FIXED VULNERABILITY 6: INSUFFICIENT LOGGING AND MONITORING ---
def payment(amount, user_id):
    logging.info(f"Processing payment of {amount} for user {user_id}")
    if amount > 1000:
        logging.warning(f"Large payment of {amount} for user {user_id}")
    return "Payment processed."

# --- FIXED VULNERABILITY 7: INSECURE DESERIALIZATION ---
def deserialization(encoded_data):
    data = base64.b64decode(encoded_data)
    return json.loads(data.decode('utf-8'))

# --- FIXED VULNERABILITY 9: INVALID REDIRECTS AND FORWARDS ---
@app.route('/redirect')
def url_redirect():
    url = request.args.get('url')
    if url.startswith('https://example.com/'):
        return redirect(url)
    return "Invalid redirect URL", 400

if __name__ == '__main__':
    app.run()