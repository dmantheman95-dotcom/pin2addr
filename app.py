import os
from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

# Load PINs from CSV
PIN_ADDRESSES = {}
with open("pins.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        PIN_ADDRESSES[row["pin"]] = row["address"]

# Get Google API key from environment
GOOGLE_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

@app.route("/")
def pin_entry():
    return render_template("pin_entry.html")

@app.route("/submit_pin", methods=["POST"])
def submit_pin():
    pin = request.form.get("pin")
    address = PIN_ADDRESSES.get(pin)
    if not address:
        return render_template("pin_entry.html", error="PIN not found")
    return redirect(url_for("show_map", pin=pin))

@app.route("/map/<pin>")
def show_map(pin):
    address = PIN_ADDRESSES.get(pin)
    if not address:
        return "PIN not found", 404
    return render_template("map_page.html", address=address, google_api_key=GOOGLE_API_KEY)

if __name__ == "__main__":
    app.run(debug=True)
