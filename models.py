from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime,date

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(64), nullable=True)
    is_admin = db.Column(db.Boolean, nullable = False, default = False)

class Lot(db.Model):
    __tablename__ = 'lot'
    lot_id = db.Column(db.Integer, primary_key=True)
    prime_loc = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    pincode = db.Column(db.CHAR(6), nullable=False)
    price_per_hr = db.Column(db.Double(),nullable = False)
    max_spots = db.Column(db.Integer,nullable=False)
    is_shaded = db.Column(db.Boolean, default=False)

    spots = db.relationship('Spot', backref = 'lot', cascade ="all, delete-orphan", lazy=True)

class Spot(db.Model):
    __tablename__ = 'spot'
    spot_id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('lot.lot_id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.CHAR(1), nullable=False, default='a')

class Reserve(db.Model):
    __tablename__ = 'reserve'
    reserve_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('lot.lot_id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('spot.spot_id'), nullable=False)
    start_time = db.Column(db.DateTime,nullable=False, default=datetime.now)
    end_time = db.Column(db.DateTime, nullable=True)
    price_per_hr = db.Column(db.Double, nullable=False)
    vehicle_num = db.Column(db.String(15), nullable=False)
    is_ongoing = db.Column(db.Boolean, nullable = False, default = True)

class Payment(db.Model):
    __tablename__ = 'payment'
    payment_id = db.Column(db.Integer, primary_key=True)
    reserve_id = db.Column(db.Integer, db.ForeignKey('reserve.reserve_id'), nullable=False)
    total_amt = db.Column(db.Double, nullable=False)
    payment_method = db.Column(db.String, nullable = True)
    transaction_date = db.Column(db.DateTime, nullable = True)


with app.app_context():
    db.create_all()
    #if admin exists, else create admin
    admin = User.query.filter_by(is_admin = True).first()
    if not admin:
        passhash = generate_password_hash('admin')
        admin = User(email = 'admin@lotandfound.com', password = passhash, name = 'Admin', is_admin=True)
        db.session.add(admin)
        db.session.commit()