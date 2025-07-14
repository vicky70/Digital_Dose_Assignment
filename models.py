
from flask_sqlalchemy import SQLAlchemy

# ()
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user')

    created_tickets = db.relationship(
        'Tickets',
        foreign_keys='Tickets.user_email',
        backref='creator',
        lazy=True
    )

    assigned_tickets = db.relationship(
        'Tickets',
        foreign_keys='Tickets.assigned_to_id',
        backref='assignee',
        lazy=True
    )


class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    issue_subject = db.Column(db.String(200), nullable=False)
    issue_description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(50), default='Open')
    resolution_note = db.Column(db.Text)

    user_email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)

    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'))