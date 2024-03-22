from app import app, usuarios
from flask import Flask, render_template, request, redirect, session,url_for
import pymongo
@app.route("/")     #funcion que accede al login.html
def Login():
    return render_template ("login.html")

@app.route("/", methods=["POST"])   #ruta inicial. entra a la bd, valida correo y contraseña a traves de una consulta
def login ():
   
    mensaje=None
    estado=None
    try:
        correo  = request.form["correo"]
        contraseña = request.form["contraseña"]
        consulta = {"correo":correo, "contraseña":contraseña}
        user = usuarios.find_one(consulta)

        # Si el usuario existe (autenticación exitosa), establecer la sesión y redirigir a la ruta 'home'
        if (user):
            session["correo"]=correo
            return redirect (url_for("home"))
        else:
            mensaje = "Datos no validos"   
    except pymongo.errors as error:
        mensaje = error
    return render_template("login.html",estado=estado,mensaje=mensaje)