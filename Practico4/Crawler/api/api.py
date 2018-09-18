from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import json

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'diario'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/diario'

mongo = PyMongo(app)

@app.route('/noticias/', methods=['GET'])
def get_noticias():
  noticia = mongo.db.noticia
  output = []
  for n in noticia.find():
    output.append({'id' : n['id'], 'categoria':n['categoria'], 'titulo' : n['titulo'], 'cuerpo':n['cuerpo'], 'hits':n['hits']})
  return json.dumps(output,ensure_ascii=False)

@app.route('/noticias/<id>', methods=['GET'])
def get_noticia(id):
  noticia = mongo.db.noticia
  n = noticia.find_one({'id' : int(id)})
  if n:
    output = {'id' : n['id'], 'categoria':n['categoria'],  'titulo' : n['titulo'], 'cuerpo':n['cuerpo'], 'hits':n['hits']}
  else:
    output = "No existe esa noticia"
  return json.dumps(output,ensure_ascii=False)

@app.route('/noticias/categoria/<categoria>/', methods=['GET'])
def get_noticias_categoria(categoria):
    noticia = mongo.db.noticia
    output = []
    for n in noticia.find({'categoria': categoria.upper()}):
        output.append({'id' : n['id'], 'categoria':n['categoria'], 'titulo' : n['titulo'], 'cuerpo':n['cuerpo'], 'hits':n['hits']})
    return json.dumps(output,ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True)