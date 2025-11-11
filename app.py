from flask import Flask, request, jsonify, render_template
import csv
import os
import urllib.parse

app = Flask(__name__)

DATA_FILE = "pins.csv"

def load_pin_map(path=DATA_FILE):
    m = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pin = row.get('pin','').strip()
            addr = row.get('address','').strip()
            if pin and addr:
                m[pin] = addr
    return m

pin_map = load_pin_map()

def validate_pin(pin):
    return pin.isdigit() and len(pin) == 4

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/lookup", methods=["POST"])
def lookup():
    data = request.get_json(silent=True)
    pin = data.get("pin") if data else None
    if not validate_pin(str(pin)):
        return jsonify({"error": "Invalid PIN"}), 400
    address = pin_map.get(pin)
    if not address:
        return jsonify({"found": False}), 404
    return jsonify({"found": True, "address": address})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
