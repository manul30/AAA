

#from crypt import methods
import json
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS, cross_origin
#from bson import ObjectId
from nlu import nlu
from tweeter_scraping import twitterFind
from youtube_scraping import findYoutube

# Instantiation
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/proyecto'
mongo = PyMongo(app)
# Settings
CORS_ALLOW_ORIGIN="*,*"
CORS_EXPOSE_HEADERS="*,*"
CORS_ALLOW_HEADERS="content-type,*"
cors = CORS(app, origins=CORS_ALLOW_ORIGIN.split(","), allow_headers=CORS_ALLOW_HEADERS.split(",") , expose_headers= CORS_EXPOSE_HEADERS.split(","),   supports_credentials = True)

# Database
db = mongo.db.usuarios
db2 = mongo.db.proyectos


### ----------- LIMPIEZA DE YOUTUBE DATA ------------- ###

def cleanYoutubeData(data):
  youtubeResults= []
  #print(type(data))
  #print(len(data['items']))
  for i in range(len(data['items'])):
    d = {}
    authorName = data['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName']
    authorChannelUrl = data['items'][i]['snippet']['topLevelComment']['snippet']['authorChannelUrl']
    likeCount = data['items'][i]['snippet']['topLevelComment']['snippet']['likeCount']
    comment = data['items'][i]['snippet']['topLevelComment']['snippet']['textDisplay']
    d['authorName'] = authorName
    d['authorChannelUrl'] = authorChannelUrl
    d['likeCount'] = likeCount
    d['comment'] = comment
    youtubeResults.append(d)
  return youtubeResults

def nlu_data(data):
  twitter = data['twitter_results']
  youtube = data['youtube_results']
  nlu_twitter = {}
  nlu_youtube= {}
  aux = 0
  if twitter['meta']['result_count'] != 0:
    for i in twitter['data']:
      try:
        analysis_json = nlu(i['text'])
      except:
        continue
      nlu_twitter['result_'+i['id']] = analysis_json
  
  for i in range(len(youtube.keys())):
    for j in youtube['video_'+str(i)]:
      try:
        analysis_json = nlu(j['comment'])
      except:
        continue
      nlu_youtube['result_'+str(aux)] = analysis_json
      aux +=1
  response = [nlu_twitter, nlu_youtube]
  return response

# PONDERADO DE SOCIAL MEDIA LISTENING
def social_listening(id):
  proyecto = db2.find_one({'_id': ObjectId(id)})
  temp = []
  sentiment = []
  emotion = []
  suma = 0
  suma2 = 0
  
  print(type(proyecto['nlu_twitter']))
  for i in proyecto['nlu_twitter'].keys():
    temp.append(proyecto['nlu_twitter'][i])
    a =temp[len(temp)-1]['keywords']
    try:
      sentiment.append(a[0]['sentiment'])
      emotion.append(a[0]['emotion'])
    except:
      pass
  for i in sentiment:
    suma+=i['score']
  suma=suma/len(sentiment)
  sadness = 0
  disgust = 0
  fear = 0
  joy = 0
  anger = 0
  for i in emotion:
    sadness+=i['sadness']
    anger+=i['anger']
    disgust+=i['disgust']
    fear+=i['fear']
    joy+=i['joy']
  emotion = {
    'ovr_sentiment': suma, 
    'sadness': sadness/len(emotion),
    'disgust': disgust/len(emotion),
    'fear': fear/len(emotion),
    'joy': joy/len(emotion),
    'fear': fear/len(emotion)
  }
  db2.update_one({'_id': ObjectId(id)}, {"$set": {
    'total_results': emotion 
  }})
  return



### ----------- ANALISIS DE SENTIMIENTO ------------- ###

@app.route('/prueba', methods=['GET'])
def prueba():
  return "Hello World!!"

@app.route('/nlu', methods=['GET'])
def sentimental_analysis(id):       # id del proyecto
  proyecto = db2.find_one({'_id': ObjectId(id)})
  [nlu_twitter, nlu_youtube]= nlu_data(proyecto)
  db2.update_one({'_id': ObjectId(id)}, {"$set": {
    'nlu_twitter': nlu_twitter, 
    'nlu_youtube': nlu_youtube
  }})
  return 

#####################################################################################################
#############################---------------- ROUTES -------------------#############################
#####################################################################################################

#-------######################-------#
#-------## REQUEST DE ADMIN ##-------#
#-------######################-------#

### --------- REGISTRO DE NUEVO SUARIO ----------- ###

# Función para la creacion o registro de usuarios
@app.route('/users', methods=['POST'])
def createUser():
  print(request.json)
  print(request.json['tipo'])
  id = db.insert_one({
    'avatar_url': "https://i.imgur.com/hepj9ZS.jpg",
    'name': request.json['name'],
    'email': request.json['email'],
    'password': request.json['password'],  
    'intentos': request.json['intentos'],  # enviar un numero por defecto i.e. 3, pero el admin q pueda modificar
    'tipo': "admin" if request.json['tipo'] else "client"   # enviar "" para ser cliente, sino "admin" para ser admin
  })
  print(id.inserted_id)
  return str(id.inserted_id)

### --------- LISTAR USUARIOS ----------- ###

# Funcion para la consulta de usuarios
@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    print("consulta get /users")
    for doc in db.find():
      #print(doc['avatar_url'] if doc['avatar_url'] else "")
      try:
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'avatar_url': doc['avatar_url'] ,
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password'],
            'intentos': doc['intentos'],
            'tipo': doc['tipo']
          })
      except:
        try:
          users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password'],
            'intentos': doc['intentos'],
            'tipo': doc['tipo']
          })
        except:
          users.append({
            '_id': str(ObjectId(doc['_id'])),
              'name': doc['name'],
              'email': doc['email'],
              'password': doc['password'],
              'intentos': doc['intentos'],
              #'tipo': doc['tipo']
          })
    return jsonify(users)

### --------- LISTAR PROYECTOS ----------- ###

# Funcion para la consulta de usuarios
@app.route('/projects', methods=['GET'])
def getProjects():
    projects = []
    print("consulta get /projects")
    for doc in db2.find():
      try:
        projects.append({
          '_id': str(ObjectId(doc['_id'])),
          'usuario' : doc['usuario'],
          'mainWord' : doc['mainWord'],
          'tags' : doc['tags'],
          'twitter_results': doc['twitter_results'],
          'youtube_results': doc['youtube_results']
        })
      except:
        pass
    return jsonify(projects)

### --------- LISTAR USUARIO POR ID ----------- ###

# Funcion para la consulta especifica de usuario
@app.route('/users/<id>', methods=['GET'])
def getUser(id):
  user = db.find_one({'_id': ObjectId(id)})
  print(user)
  return jsonify({
      '_id': str(ObjectId(user['_id'])),
      'name': user['name'],
      'email': user['email'],
      'password': user['password']
})

### --------- ELIMINAR USUARIO POR ID ----------- ###

# Funcion para eliminar un usuario especifico
@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
  db.delete_one({'_id': ObjectId(id)})
  return jsonify({'message': 'User Deleted'})

### --------- EDITAR USUARIO POR ID ----------- ###

# Funcion para editar un usuario en especifico
@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
  print(request.json)
  db.update_one({'_id': ObjectId(id)}, {"$set": {
    'name': request.json['name'],
    'email': request.json['email'],
    'password': request.json['password']
  }})
  return jsonify({'message': 'User Updated'})


#-------################################-------#
#-------## REQUEST DE ADMIN Y CLIENTE ##-------#
#-------################################-------#

### ----------- LOGIN ------------- ###

@app.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
  user = db.find_one({'email': request.json['email']})
  print(type)
  if user == None:
    return jsonify(str("NOT FOUND"))
  if request.json['password'] == user['password']:
    return jsonify(str(user))
  
### ---------- PROYECTO ------------ ###
@app.route('/project/<id>', methods=['GET'])
def getProject(id):
  proyecto = db2.find_one({'_id': ObjectId(id)})
  print(proyecto)
  return jsonify({
      '_id': str(ObjectId(proyecto['_id'])),
      'mainWord': proyecto['mainWord'],
      'tags': proyecto['tags'],
      'twitter_results': proyecto['twitter_results'],
      'youtube_results': proyecto['youtube_results'],
      'nlu_twitter': proyecto['nlu_twitter'],
      'nlu_youtube': proyecto['nlu_youtube']
})


### ----------- SCRAPING ------------- ###

@app.route('/scraping',methods=['POST'])
def web_scraping():
  mainWord = request.json['mainWord']
  tags = request.json['tags']
  response = {}
  twitter = twitterFind(mainWord, tags)
  youtube = findYoutube(mainWord, tags)
  response['twitter'] = twitter
  temp = {}
  for i in range(len(youtube.keys())):
    aux = youtube[list(youtube.keys())[i]]
    temp['video_'+str(i)] = cleanYoutubeData(aux)
  response['youtube'] = temp
  id = db2.insert_one({
    'usuario' : 'xxxxxxxxxxx',
    'mainWord' : mainWord,
    'tags' : tags,
    'twitter_results': twitter,
    'youtube_results': temp
  })
  sentimental_analysis(str(id.inserted_id))
  social_listening(str(id.inserted_id))
  return str(id.inserted_id)

if __name__ == "__main__":
    app.run(debug=True)
