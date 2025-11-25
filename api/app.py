import os
from flask import Flask, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

db_user = os.environ.get("POSTGRES_USER", "camera_user")
db_password = os.environ.get("POSTGRES_PASSWORD", "changeme")
db_name = os.environ.get("POSTGRES_DB", "camera_db")
db_host = os.environ.get("DB_HOST", "db")
db_port = os.environ.get("DB_PORT", "5432")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Camera(db.Model):
    __tablename__ = "cameras"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ip_address": self.ip_address,
            "status": self.status,
            "location": self.location,
        }

REQUEST_COUNT = Counter(
    "api_requests_total", "Total number of API requests"
)

@app.route("/health", methods=["GET"])
def health():
    REQUEST_COUNT.inc()
    return jsonify({"status": "ok"}), 200

@app.route("/cameras", methods=["GET"])
def get_cameras():
    REQUEST_COUNT.inc()
    cameras = Camera.query.order_by(Camera.id).all()
    return jsonify([c.to_dict() for c in cameras])

@app.route("/cameras/<int:camera_id>", methods=["GET"])
def get_camera(camera_id):
    REQUEST_COUNT.inc()
    camera = Camera.query.get_or_404(camera_id)
    return jsonify(camera.to_dict())

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
