from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_jwt_extended import create_access_token
from models import db, User

auth_bp = Blueprint('auth_bp', __name__, template_folder='../templates')

# Register: supports form (browser) and JSON (API)
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    # POST: accept form or JSON
    data = request.get_json(silent=True) or request.form
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        if request.is_json:
            return jsonify({"msg": "Missing fields"}), 400
        flash("Please fill all fields")
        return redirect(url_for('auth_bp.register'))

    if User.query.filter((User.username == username) | (User.email == email)).first():
        if request.is_json:
            return jsonify({"msg": "User already exists"}), 409
        flash("Username or email already exists")
        return redirect(url_for('auth_bp.register'))

    hashed = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed)
    db.session.add(user)
    db.session.commit()

    if request.is_json:
        return jsonify({"msg": "User created"}), 201
    flash("Registered successfully. Please log in.")
    return redirect(url_for('auth_bp.login'))

# Login: sessions for browser, JSON response (token) for API
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    data = request.get_json(silent=True) or request.form
    # Accept either username or email login (prefer username)
    username = data.get('username') or data.get('email')
    password = data.get('password')
    if not username or not password:
        if request.is_json:
            return jsonify({"msg": "Missing credentials"}), 400
        flash("Missing credentials")
        return redirect(url_for('auth_bp.login'))

    user = User.query.filter((User.username == username) | (User.email == username)).first()
    if not user or not check_password_hash(user.password, password):
        if request.is_json:
            return jsonify({"msg": "Invalid credentials"}), 401
        flash("Invalid credentials")
        return redirect(url_for('auth_bp.login'))

    # If client requested JSON -> return JWT
    if request.is_json:
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token}), 200

    # Otherwise perform session login for browser
    login_user(user)
    return redirect(url_for('todo_bp.todos_page'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))
