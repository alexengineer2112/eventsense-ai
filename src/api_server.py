from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "data/placement_results.json"


@app.route("/jobs")
def get_jobs():

    if not os.path.exists(DATA_FILE):
        return jsonify([])

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(port=5000)