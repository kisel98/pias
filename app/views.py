from flask import render_template, session, redirect, request, Request, jsonify
import requests
from . import app
from . import database as db

def get_profit():
    select_e_query = f'SELECT SUM(total) AS total_exp FROM expenses'
    select_i_query = f'SELECT SUM(total) AS total_in FROM incomes'

    db.cursor.execute(select_e_query)
    expense = db.cursor.fetchone()[0]
    if expense == None:
        expense = 0

    db.cursor.execute(select_i_query)
    income = db.cursor.fetchone()[0]
    if income == None:
        income = 0

    return income - expense

def get_username():
    select_query = f'SELECT firstname, lastname FROM users WHERE id = "{session.get("is_logged_in")}"'
    db.cursor.execute(select_query)
    name = db.cursor.fetchone()

    return f'{name[0]} {name[1]}'

@app.route('/')
def home():
    if not session.get('is_logged_in'):
        return redirect('/login')
    else:
        return redirect('/products')

    if session.get('is_logged_in'):
        profit = get_profit()

    return render_template('index.html', profit = profit)


@app.route('/signup', methods=['GET'])
def signup():
    if session.get('is_logged_in'):
        return redirect('/products')
        
    return render_template('signup.html', title = 'Регистрация')


@app.route('/login', methods=['GET'])
def login():
    if session.get('is_logged_in'):
        return redirect('/products')

    return render_template('login.html', title = 'Вход')


@app.route('/incomes', methods=['GET'])
def incomes():
    if not session.get('is_logged_in'):
        return redirect('/login')

    profit = get_profit()
    name = get_username()

    select_prod_query = f'SELECT name FROM products WHERE user_id = "{session.get("is_logged_in")}"'

    db.cursor.execute(select_prod_query)
    product = db.cursor.fetchall()

    select_income_query = f'SELECT * FROM incomes WHERE user_id = "{session.get("is_logged_in")}"'

    db.cursor.execute(select_income_query)
    incomes = db.cursor.fetchall()

    return render_template('incomes.html', title = 'Приходы', incomes = incomes, products = product, profit = profit, name = name)


@app.route('/expenses', methods=['GET'])
def expenses():
    if not session.get('is_logged_in'):
        return redirect('/login')

    profit = get_profit()
    name = get_username()

    select_prod_query = f'SELECT name FROM products WHERE user_id = "{session.get("is_logged_in")}"'

    db.cursor.execute(select_prod_query)
    product = db.cursor.fetchall()

    select_expense_query = f'SELECT * FROM expenses WHERE user_id = "{session.get("is_logged_in")}"'

    db.cursor.execute(select_expense_query)
    expenses = db.cursor.fetchall()

    return render_template('expenses.html', title = 'Расходы', expenses = expenses, products = product, profit = profit, name = name)


@app.route('/products', methods=['GET'])
def products():
    if not session.get('is_logged_in'):
        return redirect('/login')

    profit = get_profit()
    name = get_username()
    
    select_prod_query = f'SELECT * FROM products WHERE user_id = "{session.get("is_logged_in")}"'

    db.cursor.execute(select_prod_query)
    product = db.cursor.fetchall()

    return render_template('products.html', title = 'Продукты', products = product, profit = profit, name = name)
