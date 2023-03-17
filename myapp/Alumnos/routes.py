from flask import Flask, redirect, render_template
from flask import request
from flask import url_for
from flask import Blueprint
import forms.forms

from flask import jsonify
from config.config import DevelopmentConfig
from flask_wtf.csrf import CSRFProtect
from models.models import db #ORM
from models.models import Alumnos
from config.db import get_connection

alumnos = Blueprint('alumnos', __name__)

@alumnos.route('/regAlum', methods=['GET','POST'])
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

@alumnos.route('/modificar', methods=['GET','POST'])
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
        return redirect(url_for('alumnos.ABCompleto'))
    return render_template('modificar.html',form=create_form)

@alumnos.route('/eliminar', methods=['GET','POST'])
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
        return redirect(url_for('alumnos.ABCompleto'))
    return render_template('eliminar.html',form=create_form)

@alumnos.route("/ABCompleto", methods=["GET", "POST"])
def ABCompleto():
    create_form=forms.UserForm(request.form)
    alumnos=Alumnos.query.all()
    return render_template('ABCompleto.html',form=create_form,alumnos=alumnos)