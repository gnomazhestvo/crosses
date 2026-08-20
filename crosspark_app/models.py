from . import db
from datetime import datetime

class Cross(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    price_male = db.Column(db.Float)
    price_princess = db.Column(db.Float)
    description = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256), nullable=False)
    rating = db.Column(db.Float, default=1200.0)
    place_on_leaderboard = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)