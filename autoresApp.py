from flask import Flask,request,render_template
from pymongo import MongoClient
import json
from logger import exception

app = Flask(__name__)

@app.route("/buscarAutor",methods=['POST'])
def buscarInfoAutor():
    nombreAutor = request.get_json()['nombre']
    #coneccion mongo
    coneccion = MongoClient('127.0.0.1',27017)
    db = coneccion.test
    #busqueda autor
    if nombreAutor is not None:
        autor = db.autores.find_one({'Nombre':nombreAutor})
        respuesta={'Nombre': autor["Nombre"],
        'pais':autor["pais"],
        'sexo':autor["sexo"],
        'anno nascimineto':autor["anno nascimineto"],
        'cantidad de libros':autor["cantidad de libros"]}
    else:
        respuesta={"Nombre":""}


    return json.dumps(respuesta)


if __name__ == "__main__":
    app.run(host='localhost', port=5001)
