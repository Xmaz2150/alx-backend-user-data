#!/usr/bin/env python3
"""
Module of Session Assign and Auth
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Logs user in and creates session
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User().search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    n_user = None
    for user in users:
        if user.is_valid_password(password):
            n_user = user
        else:
            return jsonify({"error": "wrong password"}), 401

    else:
        from api.v1.app import auth

        session_id = auth.create_session(n_user.id)
        resp = make_response(user.to_json())
        cookie_key = os.getenv('SESSION_NAME', None)
        resp.set_cookie(cookie_key, session_id)
        return resp
