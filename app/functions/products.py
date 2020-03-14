from flask import jsonify, request, session, abort, make_response, redirect
from .. import app
from .. import database as db

@app.route('/api/products', methods = ['POST'])
def api_products():
    name = request.form.get('prodname')
    price = request.form.get('price')

    select_query = f'SELECT * FROM products WHERE name = "{name}" AND user_id = "{session.get("is_logged_in")}"'

    db.cursor.execute(select_query)
    product = db.cursor.fetchone()

    if product:
        return redirect('/products')

    create_query = f'INSERT INTO products (name, qty, ppp, user_id) VALUES ("{name}", 0, "{price}", "{session.get("is_logged_in")}")'

    db.cursor.execute(create_query)
    db.conn.commit()

    return redirect('/products')

@app.route('/api/products/remove/<id>', methods = ['POST'])
def api_product_remove(id):
    delete_query = f'DELETE FROM products WHERE id = "{id}" AND user_id = "{session.get("is_logged_in")}"'

    db.cursor.execute(delete_query)

    return redirect('/products')
