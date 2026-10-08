import os
from flask import Flask, jsonify
from pymongo import MongoClient
 
app = Flask(__name__)
 
# The connection string comes from an environment variable,
# never written in the code (same idea as TripTick's .env files).
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/")
APP_VERSION = os.environ.get("APP_VERSION", "dev")
 
client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=2000)
db = client["helloapp"]
 
 
@app.route("/")
def home():
    # Every visit adds 1 to a counter stored in MongoDB
    result = db.visits.find_one_and_update(
        {"_id": "home"}, {"$inc": {"count": 1}}, upsert=True, return_document=True
    )
    count = result["count"] if result else 1
    return f"<h1>Hello from Mussawer pipeline v3 - auto!</h1><p>Version: {APP_VERSION}</p><p>Visits saved in MongoDB: {count}</p>"
 
 
@app.route("/health")
def health():
    # Jenkins calls this after deploying to check the app is alive
    try:
        client.admin.command("ping")
        return jsonify(status="ok", mongo="connected", version=APP_VERSION)
    except Exception as e:
        return jsonify(status="error", mongo=str(e)), 500
 
 
def add(a, b):
    return a + b
 
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)