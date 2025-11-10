from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80))
    password_hash = db.Column(db.String(128))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    runtime = db.Column(db.Integer)
    language = db.Column(db.String(40))
    rating = db.Column(db.String(10))

class Theater(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

class Auditorium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'))
    name = db.Column(db.String(80))

class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auditorium_id = db.Column(db.Integer, db.ForeignKey('auditorium.id'))
    row = db.Column(db.String(2))
    number = db.Column(db.Integer)
    seat_type = db.Column(db.String(20))

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    auditorium_id = db.Column(db.Integer, db.ForeignKey('auditorium.id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    base_price = db.Column(db.Float)

class ShowSeat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'))
    price = db.Column(db.Float)
    status = db.Column(db.String(10), default="available")
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    total = db.Column(db.Float)
    status = db.Column(db.String(20), default="pending")
