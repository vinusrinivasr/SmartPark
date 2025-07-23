from main import app
from flask import render_template
from application.models import *
from flask import request,redirect,session
from application.database import db
from sqlalchemy.exc import IntegrityError

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
        return redirect(f'/user/profile/{user.username}')
    if 'user' in session:
        return redirect(f'/user/profile/{session["user"]}')
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

@app.route('/admin/log-out',methods=['GET'])
def admin_logout():
    session.pop('admin',None)
    return redirect('/')

@app.route('/user/log-out',methods=['GET'])
def logout():
    session.pop('user',None)
    return redirect('/')