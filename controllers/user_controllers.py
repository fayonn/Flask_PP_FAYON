from migrate import app
from migrate import db
from models import User
from flask import request, jsonify, json
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/user/create', methods=['POST'])
def create_user():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    pw_hash = generate_password_hash(password)
    email = request.json.get('email', None)
    if username and password and email and User.query.filter_by(email=email).first() is None:
        new_user = User(username=username, email=email, password=pw_hash)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"status": 'created'}), 200

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"status": 'Email already used'}), 400
    else:
        return jsonify({"status": 'Bad data'}), 204


@app.route('/user/<id>', methods=['PUT', 'DELETE'])
def user(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return jsonify({"msg": "Not Found"}), 404

    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username:
            return jsonify({"msg": "Missing username parameter"}), 400
        if not password:
            return jsonify({"msg": "Missing password parameter"}), 400
        if username == '' or password == '':
            return jsonify({"msg": "Bad username or password"}), 401
        user.username = username
        user.password = password
        db.session.commit()
        return jsonify({"name": user.username,
                        "email": user.email}), 201
    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        # return jsonify(status='deleted', name=user.userName, email=user.email), 201
        return jsonify({"status": "deleted",  
                        "name": user.username,
                        "email": user.email}), 201


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Not Found"}), 404
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    current_user = User.query.filter_by(username=username)
    if current_user is None:
        return jsonify({"msg": "Not Found"}), 404
    for i in current_user:
        if check_password_hash(i.password, password):
            return jsonify({"status": "logged_in"}), 200
    else:
        return jsonify({"Error": "Wrong password"}), 401


@app.route('/logout', methods=['GET'])
def logout():
    return jsonify({"msg": "Successfully, you have logged out"}), 200

