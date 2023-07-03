import os
from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vault.db'
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    national_id = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128))
    phrase = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        national_id = request.form['national_id']
        password = request.form['password']
        phrase = request.form['phrase']

        if User.query.filter_by(national_id=national_id).first():
            return "User already exists"

        new_user = User(national_id=national_id, phrase=phrase)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return "User created successfully"

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        national_id = request.form['national_id']
        password = request.form['password']

        user = User.query.filter_by(national_id=national_id).first()
        if user and user.check_password(password):
            return render_template('welcome.html', phrase=user.phrase)
        else:
            return "Invalid credentials"

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", default=5000)) #type: ignore