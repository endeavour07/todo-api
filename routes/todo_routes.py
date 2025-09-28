from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Todo, User

todo_bp = Blueprint('todo_bp', __name__, template_folder='../templates')

# UI route (session-based) - rendered template with server-side data
@todo_bp.route('/todos', methods=['GET'])
@login_required
def todos_page():
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template('todos.html', todos=todos, username=current_user.username)

# UI form POST (session-based)
@todo_bp.route('/todos', methods=['POST'])
@login_required
def create_todo_ui():
    # Accept form submissions
    title = request.form.get('title')
    description = request.form.get('description', '')
    if not title:
        # Could flash error; simple redirect for now
        return redirect(url_for('todo_bp.todos_page'))
    t = Todo(title=title, description=description, user_id=current_user.id)
    db.session.add(t)
    db.session.commit()
    return redirect(url_for('todo_bp.todos_page'))

# --------------------
# API endpoints (JSON) protected by JWT (for Postman / mobile)
# Base path: /api/todos
# --------------------

@todo_bp.route('/api/todos', methods=['GET'])
@jwt_required()
def api_get_todos():
    user_id = int(get_jwt_identity())
    todos = Todo.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "done": t.done
    } for t in todos]), 200

@todo_bp.route('/api/todos', methods=['POST'])
@jwt_required()
def api_create_todo():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    title = data.get('title')
    if not title:
        return jsonify({"msg": "title required"}), 422
    todo = Todo(title=title, description=data.get('description', ''), user_id=user_id)
    db.session.add(todo)
    db.session.commit()
    return jsonify({"msg": "Todo created", "id": todo.id}), 201

@todo_bp.route('/api/todos/<int:todo_id>', methods=['PATCH'])
@jwt_required()
def api_update_todo(todo_id):
    user_id = int(get_jwt_identity())
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
    if not todo:
        return jsonify({"msg": "Todo not found"}), 404
    data = request.get_json(silent=True) or {}
    if "title" in data:
        todo.title = data.get("title")
    if "description" in data:
        todo.description = data.get("description")
    if "done" in data:
        todo.done = bool(data.get("done"))
    db.session.commit()
    return jsonify({"msg": "Todo updated"}), 200

@todo_bp.route('/api/todos/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def api_delete_todo(todo_id):
    user_id = int(get_jwt_identity())
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
    if not todo:
        return jsonify({"msg": "Todo not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"msg": "Deleted"}), 200
