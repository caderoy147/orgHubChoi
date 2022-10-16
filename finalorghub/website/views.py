from datetime import date, datetime
from multiprocessing import Event
import string
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, User
import sqlite3 as sql



from . import db

views = Blueprint('views',__name__)

@views.route('/')
def home():
  return render_template("index.html")

@views.route('/dashboard')
@login_required
def dashboard():
  # how to place data of notes into dashboard
  q = request.args.get('q')
  if q:
    notes = Note.query.filter(Note.orgName.contains(q) | Note.rationale.contains(q))
  else:
    notes = Note.query.all()
  return render_template("dashboard.html", user=current_user, notes=notes)

@views.route('/show')
@login_required
def show():
  # how to place data of notes into dashboard

  return render_template("show_all.html", notes=Note.query.all())


@views.route('/profile')
def profile():

  user = current_user
  notes = user.following
  

  return render_template("profile.html", user=current_user,notes=notes)



@views.route('/eventdetails/<note>/',methods=['GET','POST'])
def details(note):
  note = Note.query.get(note)
  if request.method == 'POST':
      user=current_user
      user.following.append(note)
      db.session.commit()
      return redirect(url_for('views.profile'))
  return render_template("eventDetails.html", user=current_user, note=note)








@views.route('/organizer',methods=['GET','POST'])
def organizer():
  if request.method == 'POST':
    orgName = request.form.get('orgName')
    eventName = request.form.get('eventName')
    rationale = request.form.get('rationale')
    eventDate= request.form.get('eventDate')
    participants = request.form.get('participants')
    deadline = request.form.get('deadline')

    if len(rationale) < 2:
      flash('Rationale is too short',category='error')
    else:
      new_note = Note(orgName=orgName, eventName=eventName, rationale=rationale, eventDate=datetime.strptime(eventDate, "%Y-%m-%d").date()
      ,participants=participants, deadline=datetime.strptime(deadline, "%Y-%m-%d").date())
      db.session.add(new_note)
      db.session.commit()

      flash('Event Created!!',category='success')
      return redirect(url_for('views.dashboard'))





  return render_template("organizer.html",user=current_user)



  
@views.route('/profile/<note>/',methods=['POST'])
def delete(note):
  note = Note.query.get(note)
  if request.method == 'POST':
      user=current_user
      user.following.remove(note)
      db.session.commit()
      return redirect(url_for('views.profile'))
  return render_template("profile.html", user=current_user, note=note)




