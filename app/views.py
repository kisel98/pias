from flask import render_template, session, redirect, request, Request, jsonify
import requests
from . import app
from . import database as db

def get_profit():
    select_e_query = f'SELECT SUM(total) AS total_exp FROM expenses'
    select_i_query = f'SELECT SUM(total) AS total_in FROM incomes'

    db.cursor.execute(select_e_query)
    expense = db.cursor.fetchone()[0]

    db.cursor.execute(select_i_query)
    income = db.cursor.fetchone()[0]

    return income - expense


@app.route('/')
def home():
    if not session.get('is_logged_in'):
        return redirect('/login')
    else:
        return redirect('/products')

    if session.get('is_logged_in'):
        profit = get_profit()

    return render_template('index.html', profit = profit)


@app.route('/signup')
def signup():
    if session.get('is_logged_in'):
        return redirect('/products')
        
    return render_template('signup.html', title = 'Регистрация')


@app.route('/login')
def login():
    if session.get('is_logged_in'):
        return redirect('/products')

    return render_template('login.html', title = 'Вход')


@app.route('/incomes')
def incomes():
    if not session.get('is_logged_in'):
        return redirect('/login')

    profit = get_profit()

    select_prod_query = f'SELECT name FROM product'

    db.cursor.execute(select_prod_query)
    product = db.cursor.fetchall()

    select_income_query = f'SELECT * FROM incomes'

    db.cursor.execute(select_income_query)
    incomes = db.cursor.fetchall()

    return render_template('incomes.html', title = 'Приходы', incomes = incomes, products = product, profit = profit)


@app.route('/expenses')
def expenses():
    if not session.get('is_logged_in'):
        return redirect('/login')

    profit = get_profit()
    

    select_prod_query = f'SELECT name FROM product'

    db.cursor.execute(select_prod_query)
    product = db.cursor.fetchall()

    select_expense_query = f'SELECT * FROM expenses'

    db.cursor.execute(select_expense_query)
    expenses = db.cursor.fetchall()

    return render_template('expenses.html', title = 'Расходы', expenses = expenses, products = product, profit = profit)


@app.route('/products')
def products():
    if not session.get('is_logged_in'):
        return redirect('/login')

    profit = get_profit()
    
    select_prod_query = f'SELECT * FROM product'

    db.cursor.execute(select_prod_query)
    product = db.cursor.fetchall()

    return render_template('products.html', title = 'Продукты', products = product, profit = profit)
