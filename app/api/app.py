from flask import Flask, jsonify, send_from_directory
from pathlib import Path

app = Flask(__name__)

APP_NAME = "devops-dashboard"
APP_VERSION = "1.0.0"
APP_ENVIRONMENT = "development"


@app.get("/")
def dashboard():
    web_directory = Path(app.root_path).parent / "web"
    return send_from_directory(web_directory, "index.html")


@app.get("/api/health")
def health():
    return jsonify(
        {
            "application": APP_NAME,
            "version": APP_VERSION,
            "environment": APP_ENVIRONMENT,
            "status": "ok",
        }
    )


@app.get("/api/info")
def info():
    return jsonify(
        {
            "application": APP_NAME,
            "version": APP_VERSION,
            "environment": APP_ENVIRONMENT,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
