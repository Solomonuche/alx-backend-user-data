#!/usr/bin/env python3
"""
Module for session auth views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from os import getenv
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth():
    """handles all routes for the Session authentication.
    """

    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if user[0].is_valid_password(password) is False:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    response = jsonify(user[0].to_json())
    response.set_cookie(getenv('SESSION_NAME'), session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def delete_session():
    """Logout user
    """
    from api.v1.app import auth

    status = auth.destroy_session(request)
    if status:
        return jsonify({}), 200
    abort(404)
