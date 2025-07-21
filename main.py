from flask import Flask, render_template, request, redirect, session
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


# User Dashboard route
@app.route('/')
def userdashboard():
    try:
        if 'id' not in session:
            return redirect('/login')
        # user = User.query.get(session['id'])  //This query is deprecated (it's for lagacy projects)
        user = db.session.get(User, session['id'])

        status_filter = request.args.get('status')
        if status_filter:
            tickets = Ticket.query.filter_by(user_id=user.id, status=status_filter).all()
        else:
            tickets = Ticket.query.filter_by(user_id=user.id).all()
        return render_template('user_dashboard.html', tickets=tickets)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


# Raise Ticket
@app.route('/raise-ticket', methods=['POST'])
def raise_ticket():
    try:
        if 'user_id' not in session:
            return redirect('/login')

        user = User.query.get(session['id'])

        issue_subject = request.form['issue_subject']
        issue_description = request.form['issue_description']
        priority = request.form['priority']

        new_ticket = Ticket(
            name=user.username,
            user_email=user.email,
            issue_subject=issue_subject,
            issue_description=issue_description,
            priority=priority
        )
        db.session.add(new_ticket)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

# Admin Routes
@app.route('/admin')
def admin_dashboard():
    try:
        if 'user_id' not in session or session.get('role') != 'admin':
            return redirect('/login')

        all_tickets = Ticket.query.all()
        users = User.query.filter_by(role='user').all()

        return render_template('admin_dashboard.html', tickets=all_tickets, users=users)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


# update ticket
@app.route('/update-ticket/<int:ticket_id>', methods=['POST'])
def update_ticket(ticket_id):
    try:
        if 'user_id' not in session or session.get('role') != 'admin':
            return redirect('/login')

        ticket = Ticket.query.get_or_404(ticket_id)

        ticket.status = request.form['status']
        ticket.assigned_to_id = request.form.get('assigned_to_id')
        ticket.resolution_note = request.form.get('resolution_note')

        db.session.commit()
        return redirect('/admin')
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        print("Redirecting 1 ... ")
        message = ''
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            user = User.query.filter_by(email=email).first()
            print("Redirecting 2 ...")
            if user and check_password_hash(user.password, password):
                session['id'] = user.id
                session['name'] = user.name
                session['role'] = user.role
                print("Redirection 3 ... ")
                if user.role == 'admin':
                    return redirect('/admin')
                else:
                    print("Redirecting 4 ...")
                    return redirect('/')
            else:
                message = 'Invalid email or password'
        return render_template('login.html', message=message)
    except Exception as e:
        print("ERROR:- ", e)
        return f"An error occurred: {str(e)}", 500



@app.route('/registration', methods=['GET', 'POST'])
def registration():
    try:
        print("Redirecting...")
        message = ''
        if request.method == 'POST':
            print("Redirecting 2 ...")
            username = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']
            print("Redirecting 3...")
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                message = 'Email already registered.'
            else:
                hashed_password = generate_password_hash(password)
                new_user = User(name=username, email=email, phone=phone,password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                message = 'Registration successful!'
                print("Redirecting...")
                return redirect('/login')
        return render_template('registration.html', message=message)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/logout')
def logout():
    try:
        session.clear()
        return redirect('/login')
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
