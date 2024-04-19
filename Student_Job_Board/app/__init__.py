# Import Flask and create an app instance
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'

# MySQL configurations
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'student_job_board'

app.static_folder = 'static'

mysql = MySQL(app)

# Import the auth blueprint and register it with the app
from app.auth import auth
app.register_blueprint(auth)

# Import routes module and register it with the app
from app import routes
