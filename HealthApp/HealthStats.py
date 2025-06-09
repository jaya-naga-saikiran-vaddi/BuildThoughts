from flask import Flask, render_template
from config.config import *
from db import init_db
from controller.health_controller import health_bp

app = Flask(__name__)

app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB

mysql = init_db(app)

app.register_blueprint(health_bp, url_prefix="/entries")


@app.route('/')
def home():
    return render_template('healthView.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
