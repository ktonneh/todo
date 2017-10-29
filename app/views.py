import jwt
import datetime
from flask import jsonify
from flask import make_response
from flask import render_template, request
from flask_jwt import JWT, jwt_required, current_identity
from functools import wraps

from config import SECRET_KEY
from app import app, db
from .models import User, Todo
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None;
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            if not token:
                return jsonify({'message': 'Token is missing'}), 401

            try:
                data = jwt.decode(token, SECRET_KEY)
                current_user = User.query.filter_by(public_id=data['public_id']).first()
            except:
                return jsonify({'message': 'Token is invalid!!'}), 401

            return f(current_user, *args, **kwargs)

    return decorated


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Login')


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Not allowed to perform operation!'})
    users = User.query.all()
    # print(users.length())
    output = []
    for user in users:
        user_data = {'public_id': user.public_id, 'name': user.name, 'password': user.password, 'admin': user.admin}
        output.append(user_data)

    return jsonify({'users': output})


@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'User not found'})

    out_user = {'public_id': user.public_id, 'password': user.password, 'name': user.name, 'admin': user.admin}
    return jsonify({'user': out_user})


@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    # data = request.get_json()
    # hashed_password = generate_password_hash(data['password'],method='sha256')
    print('request gets here##')
    # print(jsonify(request.form))
    print(request.method)
    if request.method == 'POST':
        print('Method is Post Here')
        print('Name is$$')
        print(request.form['name'])
        hashed_password = generate_password_hash(request.form['password'], method='sha256')
        # hashed_password = generate_password_hash(request.form['password'])
        new_user = User(public_id=str(uuid.uuid4()), name=request.form['name'], password=hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User Created Successfully!!'})


@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'User not found'})

    user.admin = True
    db.session.commit()
    return jsonify({'message': 'User has been promoted!!'})


@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'User not found'})

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User Removed successfully!!'})


@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-authenticate': 'Basic realm="Login Required!!"'})

    print('Gets past step 1')
    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-authenticate': 'Basic realm="Login Required!!"'})
    print('Gets Past step 2')
    print('User Password##' + user.password)
    print('Auth Password##' + auth.password)
    print('PasswordHash##' + str(check_password_hash(user.password, auth.password)))
    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            SECRET_KEY)
        print('token##' + str(token))
        return jsonify({'token': token.decode('UTF-8')})
    print('Gets Past Last Step##')
    return make_response('Could not verify', 401, {'WWW-authenticate': 'Basic realm="Login Required!!"'})
