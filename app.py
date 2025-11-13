from flask import Flask, render_template, request, redirect, url_for
import csv
from urllib.parse import quote

app = Flask(__name__)

# Load PIN data from CSV
PIN_DATA = {}
with open("pins.csv", newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        PIN_DATA[row["pin"]] = {
            "address": row.get("address", "").strip(),
            "message": row.get("message", "").strip()
        }

@app.route("/")
def index():
    return render_template("pin_entry.html")

@app.route("/submit_pin", methods=["POST"])
def submit_pin():
    pin = request.form.get("pin")
    entry = PIN_DATA.get(pin)

    if not entry:
        return render_template("pin_entry.html", error="Invalid PIN")

    address = entry.get("address")
    message = entry.get("message")

    # CASE 1: Address + Message → show message page
    if address and message:
        return render_template("message_page.html", message=message, address=address)

    # CASE 2: Address only → open Google Maps directly
    if address and not message:
        maps_url = f"https://www.google.com/maps/dir/?api=1&origin=My+Location&destination={quote(address)}"
        return redirect(maps_url)

    # CASE 3: Message only → show message (no maps)
    if message and not address:
        return render_template("message_page.html", message=message, address=None)

    # CASE 4: Neither → invalid
    return render_template("pin_entry.html", error="Invalid PIN")

@app.route("/open_maps/<path:address>")
def open_maps(address):
    maps_url = f"https://www.google.com/maps/dir/?api=1&origin=My+Location&destination={quote(address)}"
    return redirect(maps_url)

if __name__ == "__main__":
    app.run(debug=True)
