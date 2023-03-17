from flask import Flask, redirect, render_template
from flask import request
from flask import url_for
from flask import Blueprint
from forms.forms import UserForm

from flask import jsonify
from config.config import DevelopmentConfig
from flask_wtf.csrf import CSRFProtect
from models.models import db #ORM
from models.models import Maestros
from config.db import get_connection

maestros = Blueprint('maestros', __name__)

@maestros.route('/regMaes', methods=['GET','POST'])
def regMaes(): 
    create_form=UserForm(request.form)
    if request.method=='POST':
        maes=Maestros(nombre=create_form.nombre.data,
                    apellidos=create_form.apellidos.data,
                    email=create_form.email.data)
        connection=get_connection()
        with connection.cursor() as cursor:
            cursor.execute('CALL AGREGAR_MAESTRO(%s, %s, %s)',(maes.nombre,maes.apellidos,maes.email))
        connection.commit()
        connection.close()
        return redirect(url_for('maestros.ABCompletoM'))
    return render_template('Maestros.html',form=create_form)

@maestros.route('/modificarM', methods=['GET','POST'])
def modificarM():
    create_form=UserForm(request.form)
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
        return redirect(url_for('maestros.ABCompletoM'))
    return render_template('modificarM.html',form=create_form)

@maestros.route('/eliminarM', methods=['GET','POST'])
def eliminarM():
    create_form=UserForm(request.form)
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
            cursor.execute('CALL ELIMINAR_MAESTRO(%s)', (maes.id))
        connection.commit()
        connection.close()
        return redirect(url_for('maestros.ABCompletoM'))
    return render_template('eliminarM.html',form=create_form)

@maestros.route("/ABCompletoM", methods=["GET", "POST"])
def ABCompletoM():
    create_form=UserForm(request.form)
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