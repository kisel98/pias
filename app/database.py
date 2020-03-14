from flaskext.mysql import MySQL
from . import app

mysql = MySQL()

app.config['MYSQL_DATABASE_USER']     = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'rootpass'
app.config['MYSQL_DATABASE_HOST']     = 'localhost'
app.config['MYSQL_DATABASE_DB']       = 'acc'

mysql.init_app(app)

try:
    conn = mysql.connect()
except:
    print("MySQL not working")
    exit(1)

cursor = conn.cursor()

create_users_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        firstname VARCHAR(64) NOT NULL,
        lastname VARCHAR(64) NOT NULL,
        email VARCHAR(64) NOT NULL UNIQUE KEY,
        password VARCHAR(64) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
'''

create_products_table_query = '''
    CREATE TABLE IF NOT EXISTS products (
        id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(64) NOT NULL UNIQUE KEY,
        qty INT(8),
        ppp INT(8),
        user_id VARCHAR(64) NOT NULL
    );
'''

create_incomes_table_query = '''
    CREATE TABLE IF NOT EXISTS incomes (
        id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(64),
        qty INT(8),
        ppp INT(8),
        total INT(8),
        user_id VARCHAR(64) NOT NULL
    );
'''

create_expenses_table_query = '''
    CREATE TABLE IF NOT EXISTS expenses (
        id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(64),
        qty INT(8),
        ppp INT(8),
        total INT(8),
        user_id VARCHAR(64) NOT NULL
    );
'''

cursor.execute(create_users_table_query)
cursor.execute(create_products_table_query)
cursor.execute(create_incomes_table_query)
cursor.execute(create_expenses_table_query)

conn.commit()
