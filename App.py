from flask import Flask,request,render_template
from pymongo import MongoClient
import json
from logger import exception


app = Flask(__name__)

@app.route("/")
@exception
def welcome():
    return render_template("index.html")

@app.route("/saludar",methods=['POST'])
@exception
def saludar():
    data = request.get_json()
    return "<h1>Hola "+data['nombre']+"</h1>"

@app.route("/buscarLibroPorNombre",methods=['POST'])
@exception
def buscarLibroPorNombre():
    #data = request.get_json()
    #nombre
    nombre = request.form.get("textNombreLibro")
    #coneccion a mongo
    coneccion = MongoClient('127.0.0.1',27017)
    #seleccion database
    db = coneccion.test
    #encontrar
    registro = db.registros.find_one({'title':nombre})
    if registro is not None :
        libro = {"titulo":registro["title"],"autor":registro["author"],"Precio":registro["Precio"]}
    else:
        libro="No encontrado"

    return json.dumps(libro)

@app.route("/buscarLibrosPorPrecio",methods=['POST'])
@exception
def buscarLibrosPorPrecio():
    data = request.get_json()
    #precios
    precio1 = data["precio1"]
    precio2 = data["precio2"]
    #coneccion a mongo
    coneccion = MongoClient('127.0.0.1',27017)
    #seleccion database
    db = coneccion.test
    #encontrar
    registro = db.registros.find({'Precio':{ '$gt' : precio1, '$lt' : precio2 }}).sort('Precio')
    coneccion=""
    lista=[]
    for aux in registro:
        lista.append({"titulo":aux["title"],"autor":aux["author"],"Precio":aux["Precio"]})

    return json.dumps(lista)


def listarTiposDeLibros():
    try:
        lista=[]

        coneccion= MongoClient('127.0.0.1',27017)
        collection = coneccion.test
        registros = db.registros.distinct('Tipo')
        for aux in registros:
            lista.append({"titulo":aux["title"],"autor":aux["author"],"Precio":aux["Precio"]})
    except Exception:
        logger.error("Error buscando tipos de libros")




if __name__ == "__main__":
    app.run()
