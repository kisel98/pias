from flaskext.mysql import MySQL
from . import app

mysql = MySQL()

app.config['MYSQL_DATABASE_USER']     = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_HOST']     = 'localhost'
app.config['MYSQL_DATABASE_DB']       = 'acc'

mysql.init_app(app)

try:
    conn = mysql.connect()
except:
    print("MySQL not working")
    exit(1)

cursor = conn.cursor()
