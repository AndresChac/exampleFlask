from flask import Flask,request,render_template
from pymongo import MongoClient
import json
from logger import exception
import urllib2


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
        data={"nombre":registro["author"]}
        requesti = urllib2.Request("http://localhost:5001/buscarAutor")
        requesti.add_header("Content-type","Application/json")
        try:
            response = urllib2.urlopen(requesti, json.dumps(data))
            responseJson=json.loads(response.read())
            if( responseJson is not None):
                libro["Pais autor"]=responseJson["pais"]
                libro["Anno de nacimiento:"]=responseJson["anno nascimineto"]
        except Exception as e:
            pass

    else:
        libro={"titulo":"No encontrado"}

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
    del(coneccion)
    lista=[]
    for aux in registro:
        lista.append({"titulo":aux["title"],"autor":aux["author"],"Precio":aux["Precio"]})

    return json.dumps(lista)

@app.route("/tiposDeLibros",methods=['GET','POST'])
@exception
def listarTiposDeLibros():
    lista=[]
    coneccion= MongoClient('127.0.0.1',27017)
    collection = coneccion.test
    registros = collection.registros.distinct('Tipo')
    del(coneccion)
    for aux in registros:
        lista.append(aux)

    return json.dumps(lista)




if __name__ == "__main__":
    app.run()
