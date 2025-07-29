from main import app
from flask import render_template
from application.models import *
from flask import request,redirect,session
from application.database import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

app.secret_key = 'secret-key'

ADMIN_USERNAME='admin'
ADMIN_PASSWORD='admin123'

@app.get("/")
def home():
    return redirect('/user/login')

@app.route("/user/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        data=request.form
        user=User.query.filter(User.username==data['username']).first()
        if not user:
            return render_template('user_login.html',username_error=True,password_error=False)
        if user.password!=data['password']:
            return render_template('user_login.html',username_error=False,password_error=True)
        session['user']=user.username
        return redirect(f'/user/profile')
    if 'user' in session:
        return redirect(f'/user/profile')
    return render_template('user_login.html',username_error=False,password_error=False)

@app.route("/user/sign-up",methods=['GET','POST'])
def signup():
    if request.method=='POST':
        try:
            data=request.form
            if data['password']!=data['confirm-password']:
                return render_template('signup.html',username_error=False,password_error=True)
            new_user=User(username=data['username'],password=data['password'],name=data['name'],address=data['address'],pincode=data['pincode'])
            db.session.add(new_user)
            db.session.commit()
            return render_template('success.html')
        except IntegrityError:
            return render_template('signup.html',username_error=True,password_error=False)
    return render_template('signup.html',username_error=False,password_error=False)

@app.route("/admin/login",methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        data=request.form
        if data['username']==ADMIN_USERNAME and data['password']==ADMIN_PASSWORD:
            session['admin']='admin'
            return redirect('/admin/dashboard')
        else:
            return render_template('admin_login.html',error=True)
    if 'admin' in session:
        return redirect('/admin/dashboard')
    return render_template('admin_login.html',error=False)

@app.route('/admin/dashboard',methods=['GET','POST'])
def admin_home():
    if 'admin' not in session:
        return redirect('/admin/login')
    if request.method=='POST':
        data=request.form
        if data['type']=='create-new-lot':
            new_lot=ParkingLot(location=data['location'],price=data['price'],address=data['address'],pincode=data['pincode'],max_spots=data['max_spots'])
            db.session.add(new_lot)
            db.session.commit()
            for i in range(int(data['max_spots'])):
                new_spot=ParkingSpot(lot_id=new_lot.id,status='A')
                db.session.add(new_spot)
            db.session.commit()
        elif data['type']=='view-spot':
            spot_id=data['spot_id']
            print(spot_id)
            spot=ParkingSpot.query.get(spot_id)
            lot=ParkingLot.query.get(spot.lot_id)
            db.session.delete(spot)
            lot.max_spots-=1
            db.session.commit()
    parking_lots=ParkingLot.query.all()
    parking_spots={}
    occupied={}
    address={}
    for i in parking_lots:
        occupied[i.id]=(len(ParkingSpot.query.filter((ParkingSpot.lot_id==i.id) & (ParkingSpot.status=='O')).all()))
        parking_spots[i.id]=(ParkingSpot.query.filter(ParkingSpot.lot_id==i.id).all())
        address[i.id]=ParkingLot.query.get(i.id).address
    return render_template('admin_home.html',parking_lots=parking_lots,parking_spots=parking_spots,occupied=occupied,address=address)

@app.route('/admin/create-lot',methods=['GET'])
def create_lot():
    if 'admin' not in session:
        return redirect('/admin/login')
    return render_template('create_new_lot.html')

@app.route('/admin/edit-lot/<lot_id>',methods=['GET','POST'])
def edit_lot(lot_id):
    if 'admin' not in session:
        return redirect('/admin/login')
    lot_data=ParkingLot.query.get(lot_id)
    if not lot_data:
        return '',404
    if request.method=="POST":
        data=request.form
        occupied=len(ParkingSpot.query.filter((ParkingSpot.lot_id==lot_id) & (ParkingSpot.status=='O')).all())
        if int(data['max_spots'])<occupied:
            return render_template('edit_lot.html',lot_data=lot_data,error=True,occupied=occupied)
        old=lot_data.max_spots
        lot_data.location=data['location']
        lot_data.address=data['address']
        lot_data.pincode=data['pincode']
        lot_data.price=data['price']
        lot_data.max_spots=data['max_spots']
        db.session.commit()        
        occupied_spots=ParkingSpot.query.filter((ParkingSpot.lot_id==lot_id) & (ParkingSpot.status=='A')).all()
        if old>int(data['max_spots']):
            for i in range(old-int(data['max_spots'])):
                db.session.delete(occupied_spots.pop())
            db.session.commit()
        elif old<int(data['max_spots']):
            for i in range(int(data['max_spots'])-old):
                new_spot=ParkingSpot(lot_id=lot_id,status='A')
                db.session.add(new_spot)
            db.session.commit()
        return redirect('/admin/dashboard')
    return render_template('edit_lot.html',lot_data=lot_data)

@app.route('/admin/delete-lot/<lot_id>',methods=['GET'])
def delete_lot(lot_id):
    if len(ParkingSpot.query.filter((ParkingSpot.lot_id==lot_id) & (ParkingSpot.status=='O')).all())==0:
        spots=ParkingSpot.query.filter(ParkingSpot.lot_id==lot_id)
        for spot in spots:
            db.session.delete(spot)
        db.session.commit()
        lot=ParkingLot.query.get(lot_id)
        db.session.delete(lot)
        db.session.commit()
    return redirect('/admin/dashboard')

@app.route('/admin/view-spot/<spot_id>',methods=['GET'])
def view_spot(spot_id):
    if 'admin' not in session:
        return redirect('/admin/login')
    spot=ParkingSpot.query.get(spot_id)
    if spot.status=='O':
        reservation=Reservation.query.filter(Reservation.spot_id==spot.id).first()
        username=User.query.get(reservation.user_id).username
        return render_template('view_spot.html',spot=spot,reservation=reservation,username=username)
    return render_template('view_spot.html',spot=spot)

@app.route('/admin/delete-spot/<spot_id>',methods=['GET'])
def delete_spot(spot_id):
    data=ParkingSpot.query.get(spot_id)
    lot_id=data.lot_id
    lot=ParkingLot.query.get(lot_id)
    if data.status=='A':
        db.session.delete(data)
        lot.max_spots-=1
        db.session.commit()
    return redirect('/admin/dashboard')

@app.route('/admin/users',methods=['GET'])
def users():
    if 'admin' not in session:
        return redirect('/admin/login')
    users=User.query.all()
    return render_template('admin_users.html',users=users)

@app.route('/admin/search',methods=['GET','POST'])
def search():
    if 'admin' not in session:
        return redirect('/admin/login')
    if request.method=='POST':
        data=request.form
        if data['select']=='location':
            parking_lots=ParkingLot.query.filter(ParkingLot.location.ilike(f"%{data['search']}%")).all()
        elif data['select']=='pincode':
            parking_lots=ParkingLot.query.filter(ParkingLot.pincode.ilike(f"%{data['search']}%")).all()
        else:
            parking_lots=[]
        parking_spots={}
        occupied={}
        address={}
        for i in parking_lots:
            occupied[i.id]=(len(ParkingSpot.query.filter((ParkingSpot.lot_id==i.id) & (ParkingSpot.status=='O')).all()))
            parking_spots[i.id]=(ParkingSpot.query.filter(ParkingSpot.lot_id==i.id).all())
            address[i.id]=ParkingLot.query.get(i.id).address
        return render_template('admin_search.html',parking_lots=parking_lots,parking_spots=parking_spots,occupied=occupied,address=address)
    return render_template('admin_search.html')

@app.route('/admin/log-out',methods=['GET'])
def admin_logout():
    session.pop('admin',None)
    return redirect('/')

@app.route('/user/log-out',methods=['GET','POST'])
def logout():
    if request.method=='POST':
        user_data=User.query.filter(User.username==session.get('user')).first()
        data=request.form
        if data['password']==data['confirm-password']!=user_data.password:
            user_data.password=data['password']
            db.session.commit()
            return redirect('/user/log-out')
        else:
            return redirect('/user/change-password')
    session.pop('user',None)
    return redirect('/')