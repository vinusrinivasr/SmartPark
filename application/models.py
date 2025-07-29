from main import db

class User(db.Model):
    __tablename__='user'
    user_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    username=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    name=db.Column(db.String,nullable=False)
    address=db.Column(db.String,nullable=False)
    pincode=db.Column(db.String,nullable=False)

class ParkingLot(db.Model):
    __tablename__='parking_lot'
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    location=db.Column(db.String,nullable=False)
    price=db.Column(db.Float,nullable=False)
    address=db.Column(db.String,nullable=False)
    pincode=db.Column(db.String,nullable=False)
    max_spots=db.Column(db.Integer,nullable=False)

class ParkingSpot(db.Model):
    __tablename__='parking_spot'
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    lot_id=db.Column(db.Integer,db.ForeignKey("parking_lot.id"),nullable=False)
    status=db.Column(db.String(1),nullable=False,default='A')

class Reservation(db.Model):
    __tablename__='reservation'
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    spot_id=db.Column(db.Integer,db.ForeignKey("parking_spot.id"),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("user.user_id"),nullable=False)
    parking_timestamp=db.Column(db.DateTime,nullable=False)
    leaving_timestamp=db.Column(db.DateTime)
    parking_cost=db.Column(db.Float)
    vehicle_no=db.Column(db.String,nullable=False)
