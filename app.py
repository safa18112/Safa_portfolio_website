from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# ✅ Required for flash messages
app.secret_key = "supersecretkey"

# ✅ Database config (Render + local fallback)
database_url = os.environ.get('DATABASE_URL')

if database_url:
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ MODEL (must come before create_all)
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.Text)

# ✅ Create tables
with app.app_context():
    db.create_all()

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Form submit
@app.route('/submit', methods=['POST'])
def submit():
    try:
        new_msg = Message(
            name=request.form.get('name'),
            email=request.form.get('email'),
            message=request.form.get('message')
        )
        db.session.add(new_msg)
        db.session.commit()

        # ✅ Success message
        flash("✅ Message sent successfully!")

        return redirect('/')
    except Exception as e:
        return f"Error: {e}"

# JSON view
@app.route('/messages')
def messages():
    msgs = Message.query.all()
    return {
        "messages": [
            {"name": m.name, "email": m.email, "message": m.message}
            for m in msgs
        ]
    }

# Admin page
@app.route('/admin')
def admin():
    msgs = Message.query.all()
    return render_template('admin.html', messages=msgs)

# Run locally
if __name__ == '__main__':
    app.run(debug=True)