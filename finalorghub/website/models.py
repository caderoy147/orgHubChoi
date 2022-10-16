from . import db
from flask_login import UserMixin


user_note = db.Table('user_note',
db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
db.Column('note_id', db.Integer, db.ForeignKey('note.id'))
)


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(150))
  email = db.Column(db.String(150), unique=True)
  password = db.Column(db.String(150))
  following = db.relationship('Note', secondary=user_note, backref='followers')


 

  #maybe a database that has all the notes for dashboard and if user email mathctes user note it will not show

class Note(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  orgName = db.Column(db.String(500))
  eventName = db.Column(db.String(150), unique=True)
  eventDate = db.Column(db.Date)
  deadline = db.Column(db.Date)
  participants = db.Column(db.Integer)
  rationale = db.Column(db.String(1000))

   
  def __init__(self, orgName, eventName, eventDate, deadline, participants, rationale):
    self.orgName = orgName
    self.eventName = eventName
    self.eventDate = eventDate
    self.deadline = deadline
    self.participants = participants
    self.rationale = rationale

class tempUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp_mail = db.Column(db.String(150), unique=True)
    temp_userName = db.Column(db.String(150), unique=False)
    temp_password = db.Column(db.String(150)) 

    def __init__(self, temp_mail, temp_userName, temp_password):
        self.temp_mail = temp_mail
        self.temp_userName = temp_userName
        self.temp_password = temp_password