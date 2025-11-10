from flask import Blueprint, jsonify
from ..models import Movie, Show

movie_bp = Blueprint("movies", __name__)

@movie_bp.get("/")
def get_movies():
    return jsonify([{"id": m.id, "title": m.title} for m in Movie.query.all()])

@movie_bp.get("/<int:movie_id>/shows")
def get_shows(movie_id):
    shows = Show.query.filter_by(movie_id=movie_id).all()
    return jsonify([{"id": s.id, "start": s.start_time.isoformat(), "price": s.base_price} for s in shows])
