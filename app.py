from flask import Flask, request, jsonify
import csv
import os

DATA_FILE = "pins.csv"
API_KEY = os.environ.get("API_KEY", "changeme")

app = Flask(__name__)

def load_pin_map(path=DATA_FILE):
    mapping = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pin = row.get('pin', '').strip()
            address = row.get('address', '').strip()
            if pin and address:
                mapping[pin] = address
    return mapping

pin_map = load_pin_map()

def valid_pin(pin):
    return pin.isdigit() and len(pin) == 4

@app.before_request
def require_key():
    if request.path == "/ping":
        return
    key = request.headers.get("X-API-Key")
    if key != API_KEY:
        return jsonify({"error": "unauthorized"}), 401

@app.route("/ping")
def ping():
    return jsonify({"status": "ok"})

@app.route("/pin/<pin>")
def get_pin(pin):
    if not valid_pin(pin):
        return jsonify({"error": "invalid_pin"}), 400
    addr = pin_map.get(pin)
    if not addr:
        return jsonify({"found": False}), 404
    return jsonify({"found": True, "pin": pin, "address": addr})

@app.route("/lookup", methods=["POST"])
def lookup():
    data = request.get_json(silent=True) or request.form
    pin = data.get("pin") if data else None
    if not pin or not valid_pin(pin):
        return jsonify({"error": "invalid_pin"}), 400
    addr = pin_map.get(pin)
    if not addr:
        return jsonify({"found": False}), 404
    return jsonify({"found": True, "pin": pin, "address": addr})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
