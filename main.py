from flask import Flask, request, session, jsonify, make_response  # Added jsonify and make_response
from models import db, User, Ticket
from werkzeug.security import generate_password_hash, check_password_hash
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database', 'tickets.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecretkey'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def userdashboard():
    try:
        if 'id' not in session:
            return jsonify({"error": "Unauthorized"}), 401
            
        user = db.session.get(User, session['id'])
        status_filter = request.args.get('status')
        
        if status_filter:
            tickets = Ticket.query.filter_by(user_id=user.id, status=status_filter).all()
        else:
            tickets = Ticket.query.filter_by(user_id=user.id).all()
            
        # Convert tickets to JSON-serializable format
        tickets_data = [{
            "id": ticket.id,
            "subject": ticket.subject,
            "description": ticket.description,
            "status": ticket.status,
            "priority": ticket.priority,
            "created_at": ticket.created_at.isoformat() if ticket.created_at else None
        } for ticket in tickets]
        
        return jsonify(tickets=tickets_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/raise-ticket', methods=['POST'])
def raise_ticket():
    try:
        if 'id' not in session:
            return jsonify({"error": "Unauthorized"}), 401

        user = User.query.get(session['id'])
        data = request.json

        # Validate required fields
        required_fields = ['category_id', 'issue_subject', 'issue_description']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Create new ticket with proper fields
        new_ticket = Ticket(
            user_id=user.id,  # Correct: user ID (integer)
            category_id=data['category_id'],
            subject=data['issue_subject'],
            description=data['issue_description'],
            priority=data.get('priority', 'Medium')  # Default to Medium
        )
        
        db.session.add(new_ticket)
        db.session.commit()
        
        return jsonify({
            "message": "Ticket created successfully",
            "ticket_id": new_ticket.id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/admin')
def admin_dashboard():
    try:
        if 'id' not in session or session.get('role') != 'admin':
            return jsonify({"error": "Unauthorized"}), 401

        all_tickets = Ticket.query.all()
        users = User.query.filter_by(role='user').all()

        # Convert to JSON-serializable format
        tickets_data = [{
            "id": ticket.id,
            "subject": ticket.subject,
            "status": ticket.status,
            "priority": ticket.priority,
            "user_email": ticket.user_email
        } for ticket in all_tickets]
        
        users_data = [{
            "id": user.id,
            "name": user.name,
            "email": user.email
        } for user in users]
        
        return jsonify(tickets=tickets_data, users=users_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/admin/create-user', methods=['POST'])
def admin_create_user():
    try:
        if 'id' not in session or session.get('role') not in ['admin', 'supervisor']:
            return jsonify({"error": "Unauthorized"}), 401
            
        data = request.json  # JSON data
        existing_user = User.query.filter_by(email=data['email']).first()
        
        if existing_user:
            return jsonify({"error": "Email already registered"}), 400

        hashed_password = generate_password_hash(data['password'])
        new_user = User(
            name=data['name'], 
            email=data['email'], 
            phone=data['phone'],
            password=hashed_password, 
            role=data['role']
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "message": "User created successfully",
            "user_id": new_user.id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update-ticket/<int:id>', methods=['POST'])
def update_ticket(id):
    try:
        if 'id' not in session or session.get('role') != 'admin':
            return jsonify({"error": "Unauthorized"}), 401

        ticket = Ticket.query.get_or_404(id)
        data = request.json  # JSON data

        ticket.status = data['status']
        if 'assigned_agent_id' in data:
            ticket.assigned_agent_id = data['assigned_agent_id']
        if 'resolution_summary' in data:
            ticket.resolution_summary = data['resolution_summary']

        db.session.commit()
        return jsonify({"message": "Ticket updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data['email']
        password = data['password']
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['id'] = user.id
            session['name'] = user.name
            session['role'] = user.role
            
            return jsonify({
                "message": "akshat successful",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role
                }
            })
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/registration', methods=['POST'])
def registration():
    try:
        data = request.json
        existing_user = User.query.filter_by(email=data['email']).first()
        
        if existing_user:
            return jsonify({"error": "Email already registered"}), 400

        hashed_password = generate_password_hash(data['password'])
        new_user = User(
            name=data['name'], 
            email=data['email'], 
            phone=data['phone'],
            password=hashed_password, 
            role=data.get('role', 'user')  # Default to 'user' role
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "message": "Registration successful",
            "user_id": new_user.id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/logout', methods=['POST'])
def logout():
    try:
        session.clear()
        return jsonify({"message": "Logged out successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)