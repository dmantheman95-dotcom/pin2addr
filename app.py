from flask import Flask, render_template, request
from urllib.parse import quote
import csv

app = Flask(__name__)

# Load PINs and addresses
PIN_ADDRESSES = {}
with open("pins.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        PIN_ADDRESSES[row["pin"]] = row["address"]

@app.route("/")
def pin_entry():
    return render_template("pin_entry.html")

@app.route("/submit_pin", methods=["POST"])
def submit_pin():
    pin = request.form.get("pin")
    address = PIN_ADDRESSES.get(pin)
    if not address:
        return render_template("pin_entry.html", error="PIN not found")

    # Redirect to Google Maps with destination; origin is current location
    maps_url = f"https://www.google.com/maps/dir/?api=1&destination={quote(address)}&travelmode=driving"
    return f"<script>window.location.href='{maps_url}';</script>"

if __name__ == "__main__":
    app.run(debug=True)
