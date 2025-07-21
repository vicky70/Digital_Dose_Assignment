
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, UTC

# ()
db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='User')
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    assigned_tickets = db.relationship('Ticket', backref='agent', foreign_keys='Ticket.assigned_agent_id')
    created_tickets = db.relationship('Ticket', backref='customer', foreign_keys='Ticket.user_id')

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    CATEGORIES = [
        'Vehicle Listing Issues',
        'Payment & Billing',
        'Vehicle Condition & Quality',
        'Delivery & Pickup',
        'Refund & Cancellation',
        'Technical/App Issues',
        'Other'
    ]


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.String(20), primary_key=True)  # example TKT-0000001
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Open', nullable=False)
    priority = db.Column(db.String(10), default='Medium', nullable=False)
    assigned_agent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolution_summary = db.Column(db.Text)
    
    attachments = db.relationship('Attachment', backref='ticket', lazy=True)
    notes = db.relationship('TicketNote', backref='ticket', lazy=True)
    vehicle_info = db.relationship('VehicleInfo', backref='ticket', uselist=False, lazy=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            last_ticket = Ticket.query.order_by(Ticket.id.desc()).first()
            new_id = 1 if not last_ticket else int(last_ticket.id.split('-')[-1]) + 1
            self.id = f"TKT-{new_id:06d}"

class Attachment(db.Model):
    __tablename__ = 'attachments'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.String(20), db.ForeignKey('tickets.id'), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.now)

class TicketNote(db.Model):
    __tablename__ = 'ticket_notes'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.String(20), db.ForeignKey('tickets.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    is_internal = db.Column(db.Boolean, default=True)

class VehicleInfo(db.Model):
    __tablename__ = 'vehicle_info'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.String(20), db.ForeignKey('tickets.id'), nullable=False)
    vehicle_type = db.Column(db.String(20))
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    registration_year = db.Column(db.Integer)
    listing_id = db.Column(db.String(50))
    condition = db.Column(db.String(20))