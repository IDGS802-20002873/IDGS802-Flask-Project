from flask import Flask, redirect, render_template
from flask import request
from flask import url_for
import forms 

from flask import jsonify
from config import DevelopmentConfig
from flask_wtf.csrf import CSRFProtect
from models import db #ORM
from models import Alumnos
from models import Maestros
from db import get_connection

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/regAlum', methods=['GET','POST'])
def regAlum():
    create_form=forms.UserForm(request.form)
    if request.method=='POST':
        alum=Alumnos(nombre=create_form.nombre.data,
                    apellidos=create_form.apellidos.data,
                    email=create_form.email.data)
        db.session.add(alum) #insert en db
        db.session.commit()
        return redirect(url_for('ABCompleto'))
    return render_template('Alumnos.html',form=create_form)

@app.route('/modificar', methods=['GET','POST'])
def modificar():
    create_form=forms.UserForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data=alum1.nombre
        create_form.apellidos.data=alum1.apellidos
        create_form.email.data=alum1.email
    if request.method=='POST':
        id=create_form.id.data
        alum=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum.nombre=create_form.nombre.data
        alum.apellidos=create_form.apellidos.data
        alum.email=create_form.email.data
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('ABCompleto'))
    return render_template('modificar.html',form=create_form)

@app.route('/eliminar', methods=['GET','POST'])
def eliminar():
    create_form=forms.UserForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data=alum1.nombre
        create_form.apellidos.data=alum1.apellidos
        create_form.email.data=alum1.email
    if request.method=='POST':
        id=create_form.id.data
        alum=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum.nombre=create_form.nombre.data
        alum.apellidos=create_form.apellidos.data
        alum.email=create_form.email.data
        db.session.delete(alum)
        db.session.commit()
        return redirect(url_for('ABCompleto'))
    return render_template('eliminar.html',form=create_form)

@app.route("/ABCompleto", methods=["GET", "POST"])
def ABCompleto():
    create_form=forms.UserForm(request.form)
    alumnos=Alumnos.query.all()
    return render_template('ABCompleto.html',form=create_form,alumnos=alumnos)

@app.route('/regMaes', methods=['GET','POST'])
def regMaes(): 
    create_form=forms.UserForm(request.form)
    if request.method=='POST':
        maes=Maestros(nombre=create_form.nombre.data,
                    apellidos=create_form.apellidos.data,
                    email=create_form.email.data)
        connection=get_connection()
        with connection.cursor() as cursor:
            cursor.execute('CALL AGREGAR_MAESTRO(%s, %s, %s)',(maes.nombre,maes.apellidos,maes.email))
        connection.commit()
        connection.close()
        return redirect(url_for('ABCompletoM'))
    return render_template('Maestros.html',form=create_form)

@app.route('/modificarM', methods=['GET','POST'])
def modificarM():
    create_form=forms.UserForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        maes1=db.session.query(Maestros).filter(Maestros.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data=maes1.nombre
        create_form.apellidos.data=maes1.apellidos
        create_form.email.data=maes1.email
    if request.method=='POST':
        id=create_form.id.data
        maes=db.session.query(Maestros).filter(Maestros.id==id).first()
        maes.nombre=create_form.nombre.data
        maes.apellidos=create_form.apellidos.data
        maes.email=create_form.email.data
        connection=get_connection()
        with connection.cursor() as cursor:
            cursor.execute('CALL MODIFICAR_MAESTRO(%s, %s, %s, %s)', (maes.id,maes.nombre,maes.apellidos,maes.email))
        connection.commit()
        connection.close()
        return redirect(url_for('ABCompletoM'))
    return render_template('modificarM.html',form=create_form)

@app.route('/eliminarM', methods=['GET','POST'])
def eliminarM():
    create_form=forms.UserForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        maes1=db.session.query(Maestros).filter(Maestros.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data=maes1.nombre
        create_form.apellidos.data=maes1.apellidos
        create_form.email.data=maes1.email
    if request.method=='POST':
        id=create_form.id.data
        maes=db.session.query(Maestros).filter(Maestros.id==id).first()
        maes.nombre=create_form.nombre.data
        maes.apellidos=create_form.apellidos.data
        maes.email=create_form.email.data
        connection=get_connection()
        with connection.cursor() as cursor:
            cursor.execute('CALL ELIMINAR_MAESTRO(%s, %s, %s)', (maes.nombre,maes.apellidos,maes.email))
        connection.commit()
        connection.close()
        return redirect(url_for('ABCompletoM'))
    return render_template('eliminarM.html',form=create_form)

@app.route("/ABCompletoM", methods=["GET", "POST"])
def ABCompletoM():
    create_form=forms.UserForm(request.form)
    connection=get_connection()
    with connection.cursor() as cursor:
        maestros = []
        cursor.execute('call CONSULTAR_MAESTROS()')
        resultset = cursor.fetchall()
        for row in resultset:
            maestros.append(row)
    connection.close()
    if request.method == 'POST':
        filtro=create_form.id.data
        if filtro:
            connection=get_connection()
            with connection.cursor() as cursor:
                maestros = []
                cursor.execute('call CONSULTAR_MAESTRO(%s)',(filtro))
                resultset = cursor.fetchall()
                for row in resultset:
                    maestros.append(row)
            connection.close()
            return render_template('ABCompletoM.html',form=create_form,maestros=maestros)
        else:
            connection=get_connection()
            with connection.cursor() as cursor:
                maestros = []
                cursor.execute('call CONSULTAR_MAESTROS()')
                resultset = cursor.fetchall()
                for row in resultset:
                    maestros.append(row)
                return render_template('ABCompletoM.html',form=create_form,maestros=maestros)
    return render_template('ABCompletoM.html',form=create_form,maestros=maestros)

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=3000)

