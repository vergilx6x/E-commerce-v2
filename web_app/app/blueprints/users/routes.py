from flask import render_template
import requests




from web_app.app.blueprints.users import bp as user_bp

user_id = "10080314-5c86-4569-8363-8dfe81cbc7c1"

# @user_bp.route('/user_profile/')
# def user_profile():

#     response = requests.get(f"http://127.0.0.1:5001/api/users/{user_id}")
#     response.raise_for_status()  # Raise an exception for HTTP errors
#     user = response.json()  # Parse the JSON response


#     return render_template("user_profile.html", user=user)