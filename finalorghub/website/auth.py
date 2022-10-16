from flask import Blueprint, render_template, request, flash, redirect, url_for
from website import views
from .models import User, tempUser
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, app
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
import random


auth = Blueprint('auth',__name__)
number = random.randint(1111,9999)

app.config['DEBUG'] = True
app.config['Testing'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['SECRET_KEY'] = "SADFNLIKRFNOERN"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'officialorghub@gmail.com'
app.config['MAIL_PASSWORD'] = 'tgifzzumvviplxkd'

mail = Mail(app)


@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()

    if user:
      if check_password_hash(user.password, password):
        flash('Login Successfull', category='success')
        login_user(user, remember=True)
        return redirect(url_for('views.dashboard'))

      else:
        flash('Invalid password', category='error')
    else:
      flash('User does not exist', category='error')


    



  return render_template("signin.html",user=current_user)






@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('views.home'))




@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method=='POST':
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')


    user = User.query.filter_by(email=email).first()
    if user:
      flash('Email already exists', category='error')
    elif len(email) < 4:
      flash('Email must be greater than 4 characters', category='error')
    elif len(name) < 2:
      flash('name must be greater than 2 characters', category='error')
    elif len(password) < 2:
      flash('password must be greater than 2 characters', category='error')
    else: 
      num = str(number)

      temp_new_user = tempUser(temp_mail=email, temp_userName=name, temp_password=generate_password_hash(password, method='sha256'))

      db.session.add(temp_new_user)
      db.session.commit()

      msg = Message("Your Verification Code is: " + num, sender='officialorghub@gmail.com', recipients=[email])
      mail.send(msg)

      return redirect(url_for("auth.verify", user_id=temp_new_user.id))

  return render_template("signup.html",user=current_user)


  
@auth.route("/sign-up/verification/<int:user_id>", methods=['GET','POST'])
def verify(user_id):

    if request.method == 'POST':
        verifyCode= request.form.get("value")
        val = int(verifyCode)

        if val == number:
            tempuser = tempUser.query.filter_by(id=user_id).first()


            user = User(email=tempuser.temp_mail, name=tempuser.temp_userName, password=tempuser.temp_password)

            g_email = tempuser.temp_mail

            db.session.add(user)
            db.session.delete(tempuser)
            db.session.commit()
            
            user = User.query.filter_by(email=g_email).first()

            login_user(user)
            flash('Account created')
            return redirect(url_for("views.dashboard", user=current_user))
        else:
            flash("Incorrect Code type again.")
            

    return render_template("verification.html", userID = user_id)

