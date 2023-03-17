from flask import Flask, redirect, render_template
from flask import request
from flask import url_for
import forms 

from flask import jsonify
from config.config import DevelopmentConfig
from flask_wtf.csrf import CSRFProtect
from models.models import db
from config.db import get_connection
from Maestros.routes import maestros
from Alumnos.routes import alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

app.register_blueprint(maestros)
app.register_blueprint(alumnos)

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=3000)

