from flask import jsonify, request, session, abort, make_response
from .. import app
import hashlib
from .. import database as db

@app.route('/api/login', methods = ['POST'])
def api_login():
    email = request.form.get('email')
    password = hashlib.sha256(request.form.get('password').encode()).hexdigest()

    select_user_query = f'SELECT * FROM users WHERE email = "{email}"'

    db.cursor.execute(select_user_query)
    user = db.cursor.fetchone()

    if not user:
        return make_response(jsonify({'msg': 'Пользователя не существует или пароль неверный'}), 422)

    select_query = f'SELECT * FROM users WHERE email = "{email}" AND password = "{password}"'

    db.cursor.execute(select_query)
    user_password = db.cursor.fetchone()

    if not user_password:
        return make_response(jsonify({'msg': 'Пользователя не существует или пароль неверный'}), 409)

    session['is_logged_in'] = user[0]

    return make_response(jsonify({'msg': 'Logged in'}), 200)

@app.route('/api/logout', methods = ['POST'])
def api_logout():
    session.clear()

    return make_response(jsonify(msg = 'Успешно'), 200)