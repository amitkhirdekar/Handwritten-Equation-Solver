from flask import Blueprint,request, render_template,redirect,url_for, flash
from app import db
from flask_login import login_user, login_required, logout_user
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        email = request.form['email']
        password = request.form['password']
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email = email).first()

        if not user:
            flash("User not Found. Please Check login credentials")
            return redirect(url_for("auth.login"))
        else:
            if not check_password_hash(user.password, password):
                flash("Please check your login credentials")
                return redirect(url_for("auth.login"))
        login_user(user)

        return redirect(url_for("main.file"))

@auth.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form.get("name")
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        if user :
            flash("Email Id already Registered")
            return redirect(url_for('auth.register'))

        new_user = User(email = email, name = name, password = generate_password_hash(password, method = "sha256"))
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

