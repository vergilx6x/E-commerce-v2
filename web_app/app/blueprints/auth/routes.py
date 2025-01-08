import requests
from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from web_app.app.blueprints.auth import bp as auth_bp

# Base URL of the API app
API_BASE_URL = "http://127.0.0.1:5001/api/"  # Update the URL as needed

def is_user_authenticated():
    token = session.get('token')
    if token:
        try:
            response = requests.get(f"{API_BASE_URL}/user_profile", headers={"Authorization": f"Bearer {token}"})
            if response.status_code == 200:
                return True
            elif response.status_code == 401:  # Token expired or invalid
                session.pop('token', None)
                refresh_token = session.get('refresh_token')
                if refresh_token:
                    refresh_response = requests.post(f"{API_BASE_URL}/refresh", json={"refresh_token": refresh_token})
                    if refresh_response.status_code == 200:
                        session['token'] = refresh_response.json().get('token')
                        session['refresh_token'] = refresh_response.json().get('refresh_token', refresh_token)  # Update refresh token if available
                        return True
        except requests.RequestException:
            pass
    return False

# Register Route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return render_template('register.html')

        try:
            response = requests.post(f"{API_BASE_URL}/register", json={
                "username": username,
                "password": password,
                "email": email
            })
            if response.status_code == 201:
                flash("Registration successful! Please log in.", "success")
                return redirect(url_for('auth.login'))
            flash(response.json().get("error", "Registration failed!"), "danger")
        except requests.RequestException as e:
            flash(f"Error connecting to registration service: {str(e)}", "danger")

    return render_template('register.html')

# Login Route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = 'remember' in request.form

        try:
            response = requests.post(f"{API_BASE_URL}/login", json={"username": username, "password": password})
            if response.status_code == 200:
                session['token'] = response.json().get("token")
                session['refresh_token'] = response.json().get("refresh_token")
                if remember:
                    session.permanent = True
                flash("Login successful!", "success")
                return redirect(url_for('auth.user_profile'))
            flash(response.json().get("error", "Login failed!"), "danger")
        except requests.RequestException as e:
            flash(f"Error connecting to authentication service: {str(e)}", "danger")

    return render_template('login.html')

# Logout Route
@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('token', None)
    session.pop('refresh_token', None)
    flash("Logged out successfully!", "success")
    return redirect(url_for('auth.login'))

# User Profile Route
@auth_bp.route('/user_profile', methods=['GET'])
def user_profile():
    token = session.get('token')
    if not token:
        return redirect(url_for('auth.login'))

    try:
        response = requests.get(f"{API_BASE_URL}/user_profile", headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            user_data = response.json()
            print(user_data.get('username'))
            return render_template('user_profile.html', username=user_data.get('username'))
        flash(response.json().get("error", "Unable to fetch user profile!"), "danger")
        return redirect(url_for('auth.login'))
    except requests.RequestException as e:
        flash(f"Error connecting to the profile service: {str(e)}", "danger")
        return redirect(url_for('auth.login'))

# Cart Routes
