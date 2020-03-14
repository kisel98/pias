from flask import jsonify, request, session, abort, make_response, redirect
from .. import app
from .. import database as db

@app.route('/api/expense', methods = ['POST'])
def api_expense():
    name = request.form.get('prodname')
    qty = request.form.get('qty')
    ppp = request.form.get('ppp')
    total = float(qty) * float(ppp)

    create_query = f'INSERT INTO expenses (name, qty, ppp, total, user_id) VALUES ("{name}", "{qty}", "{ppp}", "{total}", "{session.get("is_logged_in")}")'

    db.cursor.execute(create_query)
    db.conn.commit()

    update_query = f'UPDATE products SET qty = qty + {int(qty)} WHERE name = "{name}" AND user_id = "{session.get("is_logged_in")}"'
    db.cursor.execute(update_query)
    db.conn.commit()

    return redirect('/expenses')
