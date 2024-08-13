#!/usr/bin/env python3
"""
Flask entry point
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def index() -> str:
    """
    Home route
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
