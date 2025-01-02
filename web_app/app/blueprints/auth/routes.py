from flask import Blueprint, request, render_template, redirect, url_for, session, flash
import requests

from web_app.app.blueprints.auth import bp as auth_bp

API_BASE_URL = "http://127.0.0.1:5001/api"  # Adjust to your API base URL

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            response = requests.post(f"{API_BASE_URL}/login", json={"username": username, "password": password})
            response.raise_for_status()
            data = response.json()
            session['access_token'] = data['access_token']
            flash('Login successful.', 'success')
            return redirect(url_for('home.home'))
        except requests.RequestException:
            flash('Login failed. Check your username and/or password.', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        try:
            response = requests.post(f"{API_BASE_URL}/register", json={
                "email": email,
                "password": password,
                "username": username
            })
            response.raise_for_status()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except requests.RequestException:
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('register.html')

@auth_bp.route('/user_profile', methods=['GET'], strict_slashes=False)
def user_profile():
    token = session.get('access_token')
    if not token:
        flash('You need to log in to access your profile.', 'warning')
        return redirect(url_for('auth.login'))
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE_URL}/user_profile", headers=headers)
        response.raise_for_status()
        user = response.json()
        return render_template('user_profile.html', user=user)
    except requests.RequestException:
        flash('Failed to load profile. Please log in again.', 'error')
        return redirect(url_for('auth.login'))

# @auth_bp.route('/edit_profile', methods=['GET', 'POST'])
# def edit_profile():
#     token = session.get('access_token')
#     if not token:
#         flash('You need to log in to edit your profile.', 'warning')
#         return redirect(url_for('auth.login'))
    
#     if request.method == 'POST':
#         data = {
#             "email": request.form.get('email'),
#             "username": request.form.get('username'),
#             "first_name": request.form.get('first_name'),
#             "last_name": request.form.get('last_name')
#         }
#         try:
#             headers = {"Authorization": f"Bearer {token}"}
#             response = requests.put(f"{API_BASE_URL}/edit_profile", json=data, headers=headers)
#             response.raise_for_status()
#             flash('Profile updated successfully.', 'success')
#             return redirect(url_for('auth.user_profile'))
#         except requests.RequestException:
#             flash('Failed to update profile. Please try again.', 'error')
    
#     try:
#         headers = {"Authorization": f"Bearer {token}"}
#         response = requests.get(f"{API_BASE_URL}/user_profile", headers=headers)
#         response.raise_for_status()
#         user = response.json()
#         return render_template('edit_profile.html', user=user)
#     except requests.RequestException:
#         flash('Failed to load profile. Please log in again.', 'error')
#         return redirect(url_for('auth.login'))
