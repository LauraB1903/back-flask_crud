from app import app, productos, categoria, baseDatos, usuarios
from flask import Flask, render_template, request, jsonify, redirect, url_for,session
import pymongo
import os
from bson.objectid import ObjectId
import base64
from io import BytesIO
from bson.json_util import dumps
from pymongo import MongoClient
from controller.usuarioController import *

@app.route('/home')         #Funcion ruta home, esta funcion busca los productos de la bd, los almacena en un array y busca 

def home():
   # Verificar si hay una sesión activa
    if("correo"in session):
         # Obtener todos los productos de la base de datos
        listaProductos = productos.find()
        todos_productos = []
        for producto in listaProductos:     # Buscar la categoría del producto en la colección 'categoria'
            cat = categoria.find_one({'_id': ObjectId(producto['categoria'])})
            if cat:
                producto['categoria'] = cat['nombre']
                todos_productos.append(producto)
        return render_template("listarProductos.html", productos=todos_productos)
    else:
        mensaje ="Ingresa con tus datos"
        return render_template("login.html",mensaje=mensaje)
        
@app.route ("/agregarProductos")       # Definir la ruta para mostrar el formulario de agregar productos ('/agregarProductos')
def vistaAgregarProducto():
    
    if("correo"in session):
        listaCategorias = categoria.find()
        return render_template("formulario.html",categorias=listaCategorias)
    else:
        mensaje ="Ingresa con tus datos"
        return render_template("login.html",mensaje=mensaje)

@app.route("/agregarProductos", methods=["POST"])            # Definir la ruta para procesar el formulario de agregar productos (método POST)
def agregarProducto():

   
    
    mensaje = None
    estado = False
    if("correo"in session):
        try:
            codigo =int(request.form["codigo"]) 
            nombre = request.form["nombre"]
            precio = int(request.form["precio"])
            idCategoria = request.form["categoria"]
            foto =request.files["imagen"]


# Crear un diccionario con los datos del producto
            producto ={
                "codigo":codigo,
                "nombre":nombre,
                "precio":precio,
                "categoria":ObjectId(idCategoria)
            }

            resultado = productos.insert_one(producto)          # Insertar el producto en la base de datos
            if (resultado.acknowledged):
                idProducto = resultado.inserted_id
                nombreFoto = f"{idProducto}.jpg"
                foto.save(os.path.join(app.config["UPLOAD_FOLDER"],nombreFoto))
                mensaje = "El producto fue agregado correctamente"
                estado = True
                return redirect (url_for("home"))
            else:
                mensaje="Hay problemas al agregar"

            return render_template ("/formulario.html",estado= estado, mensaje=mensaje,)


        except pymongo.errors as error:
            mensaje = error
            return error
    else:
        mensaje ="Ingresa con tus datos"
        return render_template("login.html",mensaje=mensaje)
    
    
    
@app.route("/editarProducto/<producto_id>", methods=["GET"])     # Definir la ruta para editar un producto específico ('/editarProducto/<producto_id>')
def editar_p(producto_id):
   
    if "correo" in session:
        try:                 # Buscar el producto en la base de datos por su ID
            producto = productos.find_one({"_id": ObjectId(producto_id)})
            if producto:
                listaCategorias = categoria.find()
                return render_template("editarProducto.html", producto=producto, categorias=listaCategorias)
            else:
                return "Producto no encontrado."
        except pymongo.errors.PyMongoError as error:
            return f"No se puede cargar el producto: {error}"
    else:
        mensaje = "Ingresa con tus datos"
        return render_template("login.html", mensaje=mensaje)
    
@app.route("/actualizarProducto/<producto_id>", methods=["POST"])         # Definir la ruta para actualizar un producto específico ('/actualizarProducto/<producto_id>')
def actualizar_p(producto_id):         
    
    if "correo" in session:
        try:            # Obtener los datos actualizados del producto del formulario enviado por el usuario

            codigo = int(request.form["codigo"]) 
            nombre = request.form["nombre"]
            precio = int(request.form["precio"])
            idCategoria = request.form["categoria"]
            foto = request.files["imagen"]


            producto_actualizado = {          # Crear un diccionario con los datos actualizados del producto
                "codigo": codigo,
                "nombre": nombre,
                "precio": precio,
                "categoria": ObjectId(idCategoria)
            }

            productos.update_one({"_id": ObjectId(producto_id)}, {"$set": producto_actualizado})

                
            if foto:         # Guardar la nueva imagen del producto si se proporciona
                nombreFoto = f"{producto_id}.jpg"
                foto.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreFoto))

            return redirect(url_for("home"))

        except pymongo.errors.PyMongoError as error:
            return f"No se puede actualizar el producto: {error}"
    else:
        mensaje = "Ingresa con tus datos"
        return render_template("login.html", mensaje=mensaje)

    
@app.route("/eliminarProducto/<producto_id>", methods=["GET"])       # Definir la ruta para eliminar un producto específico ('/eliminarProducto/<producto_id>')
def eliminar_p(producto_id):
    
    if("correo"in session):
        try:    # Eliminar el producto de la base de datos por su ID

            resultado = productos.delete_one({"_id": ObjectId(producto_id)})
            if resultado.deleted_count == 1:
                return redirect(url_for("home"))
            else:
                return "El producto no fue encontrado."
        except pymongo.errors.PyMongoError as error:
            return f"No se puede eliminar el producto: {error}"
    else:
        mensaje ="Ingresa con tus datos"
        return render_template("login.html",mensaje=mensaje)

@app.route("/salir") # Definir la ruta para cerrar la sesión
def salir():
    session.clear()
    mensaje="Se ha cerrado sesion"
    return render_template("login.html",mensaje=mensaje)