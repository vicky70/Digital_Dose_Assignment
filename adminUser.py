
from main import app
from models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    hashed_pw = generate_password_hash("admin123")
    admin_user = User(username="admin", email="admin@example.com", password=hashed_pw, role="admin")
    db.session.add(admin_user)
    db.session.commit()