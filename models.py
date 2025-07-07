from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(256), nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(64), nullable=True)
    phone = db.Column(db.CHAR(10), nullable=True)

class Lot(db.Model):
    __tablename__ = 'lot'
    lot_id = db.Column(db.Integer, primary_key=True)
    prime_loc = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    pincode = db.Column(db.CHAR(6), nullable=False)
    price_per_hr = db.Column(db.Double(),nullable = False)
    max_slots = db.Column(db.Integer,nullable=False)
    is_shaded = db.Column(db.Boolean)

    spots = db.relationship('Spot', backref='Lot', lazy=True)

class Spot(db.Model):
    __tablename__ = 'spot'
    spot_id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('lot.lot_id'), nullable=False)
    status = db.Column(db.CHAR(1), nullable=False, default='A')

class Reserve(db.Model):
    __tablename__ = 'reserve'
    r_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('lot.lot_id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('spot.spot_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time,nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    price_per_hr = db.Column(db.Double, nullable=False)
    vehicle_num = db.Column(db.String(15), nullable=False)

'''class Payment(db.Model):
    __tablename__ = 'payment'
    payment_id = db.Column(db.Integer, primary_key=True)
    r_id = db.Column(db.Integer, db.ForeignKey('reserve.r_id'), nullable=False)
    total_amt = db.Column(db.Double, nullable=False)
    date = db.Column(db.Date)
    time = db.Column(db.Time)'''

with app.app_context():
    db.create_all()
    