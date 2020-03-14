from flask import jsonify, request, make_response
from .. import app
import hashlib
from .. import database as db

@app.route('/api/signup', methods = ['POST'])
def api_signup():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    password = hashlib.sha256(request.form.get('password').encode()).hexdigest()
    create_query = f'INSERT INTO users (firstname, lastname, email, password) VALUES ("{firstname}", "{lastname}", "{email}", "{password}")'
    select_query = f'SELECT firstname, lastname, email FROM users WHERE email = "{email}"'

    try:
        db.cursor.execute(select_query)
        user = db.cursor.fetchone()

        if user:
            return make_response(jsonify({'msg': 'User already exists'}), 422)

    except:
        return make_response(jsonify({'msg': 'Unable to create user'}), 500)

    try:
        db.cursor.execute(create_query)
        db.conn.commit()

        return jsonify({'msg': 'Thank you for registration'})
    except:
        return make_response(jsonify({'msg': 'Unable to create user'}), 500)
