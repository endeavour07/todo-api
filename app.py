from flask import Flask, redirect, url_for
from config import Config
from models import db
from routes.auth_routes import auth_bp
from routes.todo_routes import todo_bp
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

# init extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login'  # route name for login page
jwt = JWTManager(app)

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(todo_bp)  # routes inside todo_bp define /todos and /api/todos

# home: redirect to register or todos if logged in
@app.route('/')
def index():
    return redirect(url_for('auth_bp.register'))

# create tables on startup (only for dev)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
