import os
import sqlite3
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# -------------------
# App setup
# -------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")
DB_PATH = os.path.join(BASE_DIR, "vape.db")

app = Flask(__name__, static_folder=FRONTEND_DIR)
CORS(app)


# -------------------
# Database helper
# -------------------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------
# Frontend routes
# -------------------
@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


# -------------------
# API routes
# -------------------
@app.route("/products", methods=["GET"])
def products():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()

        conn.close()

        products = [dict(row) for row in rows]

        print("✅ /products API called, returned", len(products), "items")
        return jsonify(products)

    except Exception as e:
        print("❌ ERROR in /products:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/orders", methods=["POST"])
def orders():
    data = request.json

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO orders (name, address, items, total) VALUES (?, ?, ?, ?)",
            (
                data.get("name"),
                data.get("address"),
                str(data.get("items")),
                data.get("total")
            )
        )

        conn.commit()
        conn.close()

        return jsonify({"message": "Order placed successfully"})

    except Exception as e:
        print("❌ ERROR in /orders:", e)
        return jsonify({"error": str(e)}), 500


# -------------------
# Run app (IMPORTANT)
# -------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
