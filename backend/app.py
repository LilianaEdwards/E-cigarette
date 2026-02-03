import os
import sqlite3
import json
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# -------------------
# App setup
# -------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")
DB_PATH = os.path.join(BASE_DIR, "vape.db")

app = Flask(__name__)
CORS(app)

# -------------------
# Database helper
# -------------------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            items TEXT,
            total REAL,
            status TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -------------------
# Frontend routes
# -------------------
@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)

# -------------------------
# DATA (unchanged)
# -------------------------
PRODUCTS = [
    {"id":1,"name":"SMOK Nord 4","price":45000,"img":"https://tse1.mm.bing.net/th/id/OIP.eAarG4ndv1q8zFUr9ZlA6AHaE8?pid=Api&P=0&h=220","stock":1},
  {"id":2,"name":"Vaporesso Luxe Q","price":50000,"img":"https://tse1.mm.bing.net/th/id/OIP.BgEJipmTVALDgm1jecFudgHaE8?pid=Api&P=0&h=220","stock":1},
  {"id":3,"name":"GeekVape Aegis X","price":55000,"img":"https://tse1.mm.bing.net/th/id/OIP.nyS8r8hs8MXkJxsQJBoGDAHaHa?pid=Api&P=0&h=220","stock":1},
  {"id":4,"name":"Voopoo Drag X Plus","price":48000,"img":"https://tse4.mm.bing.net/th/id/OIP.U_AjzdPvDLZFwmSiBHV2_QHaDW?pid=Api&P=0&h=220","stock":1},
  {"id":5,"name":"Lost Vape Orion Q","price":47000,"img":"https://tse3.mm.bing.net/th/id/OIP.ftsop4xERXfGSr4vzcrlggHaER?pid=Api&P=0&h=220","stock":1},
  {"id":6,"name":"SMOK RPM 40","price":46000,"img":"https://tse3.mm.bing.net/th/id/OIP.qUyElTTEMEVYL95XdTtGVgHaE8?pid=Api&P=0&h=220","stock":1},
  {"id":7,"name":"Voopoo Vinci X","price":49000,"img":"https://tse4.mm.bing.net/th/id/OIP.RJpbqjOxu750Z7T5luGubQHaHa?pid=Api&P=0&h=220","stock":1},
  {"id":8,"name":"Uwell Caliburn G","price":43000,"img":"https://tse3.mm.bing.net/th/id/OIP.8ZxmfGlgv5CGG0Q-IrrxyQHaHa?pid=Api&P=0&h=220","stock":1},
  {"id":9,"name":"GeekVape Wenax K1","price":42000,"img":"https://tse4.mm.bing.net/th/id/OIP.PKeQxKdDAVIIYbq-m6f8_wHaDM?pid=Api&P=0&h=220","stock":1},
  {"id":10,"name":"Aspire PockeX","price":44000,"img":"https://tse1.mm.bing.net/th/id/OIP.7Wda3vjDmS2R3ei5Hh4aHAHaHa?pid=Api&P=0&h=220","stock":1},
  {"id":11,"name":"SMOK Mico","price":41000,"img":"https://tse2.mm.bing.net/th/id/OIP.01tcLskCz7Ddh0HkhzlsJAHaE8?pid=Api&P=0&h=220","stock":1},
  {"id":12,"name":"Voopoo Argus Air","price":47000,"img":"https://tse1.mm.bing.net/th/id/OIP.Oz6no85rEAo6cm_tOmABSQHaE8?pid=Api&P=0&h=220","stock":1},
  {"id":13,"name":"Vaporesso XROS","price":45000,"img":"https://tse1.mm.bing.net/th/id/OIP.s_q9f3l0bMvJlm473zsCFgHaHa?pid=Api&P=0&h=220","stock":1},
  {"id":14,"name":"Lost Vape Lyra","price":46000,"img":"https://tse3.mm.bing.net/th/id/OIP.QFX43avQHJbYYq43AcWFTQHaE8?pid=Api&P=0&h=220","stock":1},
  {"id":15,"name":"Uwell Caliburn Koko","price":43000,"img":"https://tse1.mm.bing.net/th/id/OIP.6_Y_XXe6tem0o6VYOYL0FQHaEK?pid=Api&P=0&h=220","stock":1},
  {"id":16,"name":"Aspire Breeze 2","price":42000,"img":"https://tse2.mm.bing.net/th/id/OIP.yXbqg94KVAKx78NSF27L0wAAAA?pid=Api&P=0&h=220","stock":1},
  {"id":17,"name":"SMOK Novo 4","price":44000,"img":"https://tse3.mm.bing.net/th/id/OIP.G9ppe5cuEZ2sHur5z6P5RgHaE0?pid=Api&P=0&h=220","stock":1},
  {"id":18,"name":"Voopoo Drag S","price":48000,"img":"https://tse4.mm.bing.net/th/id/OIP.7odI_Fc3zUe_Gq9feFgPVAHaDe?pid=Api&P=0&h=220","stock":1},
  {"id":19,"name":"GeekVape Aegis Nano","price":45000,"img":"https://tse2.mm.bing.net/th/id/OIP.EwLGypkqkuzLnXCqyjq_jwHaE7?pid=Api&P=0&h=220","stock":1},
  {"id":20,"name":"Vaporesso Target PM80","price":47000 ,"img":"https://tse3.mm.bing.net/th/id/OIP.95YrxNHx5DRNNEtLcLZh9QHaE8?pid=Api&P=0&h=220","stock":1}
]


CART = []

# -------------------------
# API ROUTES
# -------------------------
@app.route("/products")
def get_products():
    return jsonify(PRODUCTS)

@app.route("/cart", methods=["GET"])
def get_cart():
    return jsonify(CART)

@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    product = next((p for p in PRODUCTS if p["id"] == data["id"]), None)

    if not product:
        return jsonify({"success": False, "message": "Product not found"}), 400

    existing = next((i for i in CART if i["id"] == data["id"]), None)
    if existing:
        existing["qty"] += data.get("qty", 1)
    else:
        CART.append({
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "qty": data.get("qty", 1),
            "img": product["img"]
        })

    return jsonify({"success": True})

@app.route("/cart/remove/<int:pid>", methods=["POST"])
def remove_from_cart(pid):
    global CART
    CART = [i for i in CART if i["id"] != pid]
    return jsonify({"success": True})

# -------------------------
# CHECKOUT (SAFE + FIXED)
# -------------------------
@app.route("/cart/checkout", methods=["POST"])
def checkout():
    global CART

    if not CART:
        return jsonify({"success": False, "message": "Cart is empty"}), 400

    order_items = CART.copy()
    total = sum(i["price"] * i["qty"] for i in order_items)
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO orders (items, total, status, date) VALUES (?, ?, ?, ?)",
            (json.dumps(order_items), total, "PENDING", date)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print("CHECKOUT ERROR:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

    CART = []

    return jsonify({
        "success": True,
        "redirect": "/orders.html"
    })

# -------------------------
# ORDER HISTORY / ADMIN
# -------------------------
@app.route("/orders", methods=["GET"])
def get_orders():
    conn = get_db_connection()
    orders = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    conn.close()

    result = []
    for o in orders:
        result.append({
            "id": o["id"],
            "items": json.loads(o["items"]),
            "total": o["total"],
            "status": o["status"],
            "date": o["date"]
        })

    return jsonify(result)

@app.route("/order/status/<int:oid>", methods=["POST"])
def update_order_status(oid):
    data = request.get_json()
    status = data.get("status")

    if status not in ["APPROVED", "REJECTED"]:
        return jsonify({"success": False}), 400

    conn = get_db_connection()
    conn.execute("UPDATE orders SET status=? WHERE id=?", (status, oid))
    conn.commit()
    conn.close()

    return jsonify({"success": True})

# -------------------
# Run
# -------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

