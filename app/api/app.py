import os
from pathlib import Path

import mariadb
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "devops_dashboard")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_db_connection():
    return mariadb.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )


@app.get("/")
def dashboard():
    web_directory = Path(app.root_path).parent / "web"
    return send_from_directory(web_directory, "index.html")


@app.get("/api/health")
def health():
    connection = None

    try:
        connection = get_db_connection()

        return jsonify(
            {
                "application": "devops-dashboard",
                "status": "ok",
                "database": "connected",
            }
        )

    except mariadb.Error as error:
        return jsonify(
            {
                "application": "devops-dashboard",
                "status": "error",
                "database": "unavailable",
                "error": str(error),
            }
        ), 503

    finally:
        if connection:
            connection.close()


@app.get("/api/info")
def info():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT name, version, environment
            FROM applications
            LIMIT 1
            """
        )

        row = cursor.fetchone()

        if row is None:
            return jsonify(
                {
                    "application": "devops-dashboard",
                    "status": "error",
                    "message": "No application record found",
                }
            ), 404

        return jsonify(
            {
                "application": row[0],
                "version": row[1],
                "environment": row[2],
            }
        )

    except mariadb.Error as error:
        return jsonify(
            {
                "application": "devops-dashboard",
                "status": "error",
                "message": "Database query failed",
                "error": str(error),
            }
        ), 503

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
