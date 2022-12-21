from flask import Blueprint,render_template, request, flash, redirect, url_for
from . import models
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

auth=Blueprint('auth','__name__')


@auth.route('/login',methods=['GET','POST'])
def login():
    # data = request.form
    # print(data)
    # return render_template("login.html", boolean=True)
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')

        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!',category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, Try Again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", boolean=True)
    

        


@auth.route('logout')
def logout():
    return "<p>logout</>"

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if(request.method=='POST'):
        email=request.form.get('email')
        first_name=request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        user=User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif(len(email)<4):
            flash('Email must be greater than 3 characters.', category='error')
        elif(len(first_name)<2):
            flash('First Name must be greater than 1 characters.', category='error')
        elif(password1!=password2):
            flash('Passwords do not match.', category='error')
        elif(len(password1)<7):
            flash('Passwords must be at least 7 characters.', category='error')
        else:
            new_user=User(email=email, first_name=first_name, password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created!', category='success')
            return redirect('/')
            
    return render_template("sign_up.html")

