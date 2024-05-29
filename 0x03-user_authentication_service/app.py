#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", strict_slashes=False)
def index():
    """
    index route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    register user
    """
    try:
        data = request.form
        email = data.get('email')
        password = data.get('password')

        user = AUTH.register_user(email, password)
        data = {"email": f"{email}", "message": "user created"}
        return jsonify(data)
    except ValueError:
        data = {"message": "email already registered"}
        return jsonify(data), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
