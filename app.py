from flask import Flask
import pymongo

app = Flask(__name__)
app.config["UPLOAD_FOLDER"]="./static/Img"       # Configurar la carpeta de carga de archivos estáticos para las imágenes

app.secret_key = 'salchis'             # Establecer una clave secreta para la aplicación Flask (usada para sesiones)

miConexion= pymongo.MongoClient("mongodb://localhost:27017")

baseDatos = miConexion["GESTIONPRODUCTOS"]

productos = baseDatos["Productos"]
categoria = baseDatos["Categorias"]
usuarios = baseDatos["usuarios"]


# Importar controladores de usuario y productos desde sus respectivos módulos
from controller.usuarioController import *
from controller.productoController import *



if (__name__) == "__main__":
    app.run(debug=True, port=4000)