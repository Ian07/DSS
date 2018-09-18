import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#Datos de prueba
noticias = [
    {'id': 0,
     'title': 'Se ignagura el vuelo Gaiman - Dolavon',
     'seccion': 'Provincial',
     'nro_visitas': 1},
    {'id': 1,
     'title': 'Se ignagura el vuelo Gaiman - Dolavon',
     'seccion': 'Provincial',
     'nro_visitas': 2},
    {'id': 2,
     'title': 'Se ignagura el vuelo Gaiman - Dolavon',
     'seccion': 'Provincial',
     'nro_visitas': 3}
]

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

app.run()