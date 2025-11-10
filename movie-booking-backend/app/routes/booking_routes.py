from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Booking, ShowSeat
from .. import db

booking_bp = Blueprint("bookings", __name__)

@booking_bp.post("/")
@jwt_required()
def create_booking():
    user_id = get_jwt_identity()
    data = request.json
    show_id = data["show_id"]
    seat_ids = data["seat_ids"]

    with db.session.begin_nested():
        seats = (ShowSeat.query
                 .filter(ShowSeat.id.in_(seat_ids), ShowSeat.show_id == show_id)
                 .with_for_update().all())

        if len(seats) != len(seat_ids):
            return {"error": "Invalid seats"}, 400
        if any(s.status != "available" for s in seats):
            return {"error": "Some seats already booked"}, 409

        total = sum(s.price for s in seats)
        booking = Booking(user_id=user_id, show_id=show_id, total=total, status="confirmed")
        db.session.add(booking)
        db.session.flush()
        for s in seats:
            s.status = "booked"
            s.booking_id = booking.id

    db.session.commit()
    return {"msg": "Booking successful", "booking_id": booking.id, "total": total}

@booking_bp.post("/cancel/<int:booking_id>")
@jwt_required()
def cancel_booking(booking_id):
    user_id = get_jwt_identity()
    booking = Booking.query.get(booking_id)
    if not booking or booking.user_id != user_id:
        return {"error": "Not found"}, 404

    with db.session.begin_nested():
        booking.status = "cancelled"
        for s in ShowSeat.query.filter_by(booking_id=booking.id).all():
            s.status = "available"
            s.booking_id = None
    db.session.commit()
    return {"msg": "Booking cancelled"}
